from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime

from app.database.session import SessionLocal
from app.auth.security import verify_token
from app.models.profile import Profile
from app.models.evaluation import Evaluation
from app.master_service import CDSSMasterRouter

router = APIRouter(prefix="/evaluate", tags=["Evaluations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================
# RUN MULTI-PANEL EVALUATION + STORE
# =========================================

@router.post("/{profile_id}")
def run_evaluation(
    profile_id: int,
    request_body: Dict[str, Any],
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    print(f"[DEBUG] Creating evaluation for profile_id: {profile_id}")
    
    panels = request_body.get("panels", [])
    data = request_body.get("data", {})
    # Verify profile ownership
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    if profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Run panels
    results = CDSSMasterRouter.route_multiple(panels, data)

    # Extract model versions safely
    model_versions = {
        panel: result.get("model_version")
        for panel, result in results.items()
    }

    override_flag = any(
        result.get("decision_source") == "Rule Engine (Authoritative Override)"
        for result in results.values()
        if isinstance(result, dict)
    )

    # Store evaluation with transaction handling
    try:
        evaluation = Evaluation(
            profile_id=profile_id,
            panels_run=panels,
            input_payload=data,
            output_result=results,
            override_flag=override_flag,
            model_versions=model_versions,
            evaluation_version="1.0"
        )

        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)
        
        print(f"[DEBUG] Created evaluation ID: {evaluation.id} for profile_id: {profile_id}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to store evaluation: {str(e)}")

    return {
        "evaluation_id": evaluation.id,
        "timestamp": evaluation.timestamp,
        "profile_id": profile_id,
        "panels_run": panels,
        "results": results
    }


# =========================================
# PROFILE HISTORY
# =========================================

@router.get("/history/{profile_id}")
def get_profile_history(
    profile_id: int,
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    print(f"[DEBUG] Fetching history for profile_id: {profile_id}")
    
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    if profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    evaluations = db.query(Evaluation)\
        .filter(Evaluation.profile_id == profile_id)\
        .order_by(Evaluation.timestamp.desc())\
        .all()

    print(f"[DEBUG] Found {len(evaluations)} evaluations for profile {profile_id}")
    for eval in evaluations:
        print(f"  - Evaluation ID: {eval.id}, Profile ID: {eval.profile_id}")

    return evaluations


# =========================================
# GET SINGLE EVALUATION
# =========================================

@router.get("/record/{evaluation_id}")
def get_single_evaluation(
    evaluation_id: int,
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    evaluation = db.query(Evaluation)\
        .filter(Evaluation.id == evaluation_id)\
        .first()

    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    profile = db.query(Profile).filter(Profile.id == evaluation.profile_id).first()

    if profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return evaluation


# =========================================
# DELETE EVALUATION
# =========================================

@router.delete("/record/{evaluation_id}")
def delete_evaluation(
    evaluation_id: int,
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    evaluation = db.query(Evaluation)\
        .filter(Evaluation.id == evaluation_id)\
        .first()

    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    profile = db.query(Profile).filter(Profile.id == evaluation.profile_id).first()

    if profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    db.delete(evaluation)
    db.commit()

    return {"message": "Evaluation deleted successfully"}
