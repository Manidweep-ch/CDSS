from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.session import SessionLocal
from app.models.profile import Profile
from app.models.evaluation import Evaluation
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.auth.security import verify_token
from app.schemas.profile_schema import ProfileCreate, ProfileResponse

router = APIRouter(prefix="/profiles", tags=["Profiles"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================
# CREATE PROFILE
# =========================================

@router.post("/", response_model=ProfileResponse)
def create_profile(
    profile_data: ProfileCreate,
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    profile = Profile(
        user_id=current_user.id,
        profile_name=profile_data.profile_name,
        age=profile_data.age,
        gender=profile_data.gender
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


# =========================================
# LIST PROFILES (STRICT USER ONLY)
# =========================================

@router.get("/", response_model=List[ProfileResponse])
def list_profiles(
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    profiles = db.query(Profile)\
        .filter(Profile.user_id == current_user.id)\
        .all()

    return profiles


# =========================================
# GET SINGLE PROFILE (OWNERSHIP ENFORCED)
# =========================================

@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(
    profile_id: int,
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile)\
        .filter(Profile.id == profile_id)\
        .first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    if profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return profile


# =========================================
# DELETE PROFILE (STRICT OWNERSHIP)
# =========================================

@router.delete("/{profile_id}")
def delete_profile(
    profile_id: int,
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile)\
        .filter(Profile.id == profile_id)\
        .first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    if profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Delete all evaluations for this profile
    evaluations = db.query(Evaluation)\
        .filter(Evaluation.profile_id == profile_id)\
        .all()
    
    print(f"[DEBUG] Deleting {len(evaluations)} evaluations for profile {profile_id}")
    
    # Delete chat messages and sessions for each evaluation
    for evaluation in evaluations:
        # Get all chat sessions for this evaluation
        chat_sessions = db.query(ChatSession)\
            .filter(ChatSession.evaluation_id == evaluation.id)\
            .all()
        
        for session in chat_sessions:
            # Delete all messages in this session (using session.id, not session_id)
            db.query(ChatMessage)\
                .filter(ChatMessage.session_id == session.id)\
                .delete()
            
            # Delete the session
            db.delete(session)
        
        # Delete the evaluation
        db.delete(evaluation)
    
    # Finally delete the profile
    db.delete(profile)
    db.commit()

    return {"message": "Profile deleted"}
