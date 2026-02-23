from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.llm.groq_explainer import generate_explanation
from app.database.session import SessionLocal
from app.auth.security import verify_token
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.models.evaluation import Evaluation
from app.models.profile import Profile

router = APIRouter(prefix="/chat", tags=["Chat"])


# Request models
class ChatStartRequest(BaseModel):
    evaluation_id: int
    session_type: str
    panel_name: Optional[str] = None


class ChatMessageRequest(BaseModel):
    session_id: int
    message: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================
# START NEW CHAT SESSION
# =========================================

@router.post("/start")
def start_chat(
    request: ChatStartRequest,
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    evaluation = db.query(Evaluation)\
        .filter(Evaluation.id == request.evaluation_id)\
        .first()

    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    profile = db.query(Profile)\
        .filter(Profile.id == evaluation.profile_id)\
        .first()

    if profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    if request.session_type not in ["global", "panel"]:
        raise HTTPException(status_code=400, detail="Invalid session type")

    if request.session_type == "panel" and not request.panel_name:
        raise HTTPException(status_code=400, detail="panel_name required")

    chat_session = ChatSession(
        evaluation_id=request.evaluation_id,
        profile_id=evaluation.profile_id,
        session_type=request.session_type,
        panel_name=request.panel_name
    )

    db.add(chat_session)
    db.commit()
    db.refresh(chat_session)

    return {
        "session_id": chat_session.id,
        "message": "Chat session created"
    }


# =========================================
# SEND MESSAGE
# =========================================

@router.post("/message")
def send_message(
    request: ChatMessageRequest,
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    session = db.query(ChatSession)\
        .filter(ChatSession.id == request.session_id)\
        .first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    profile = db.query(Profile)\
        .filter(Profile.id == session.profile_id)\
        .first()

    if profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Store user message
    user_msg = ChatMessage(
        session_id=request.session_id,
        role="user",
        message=request.message
    )

    db.add(user_msg)

    # Load stored evaluation result
    evaluation = db.query(Evaluation)\
        .filter(Evaluation.id == session.evaluation_id)\
        .first()

    # Validate evaluation result
    if not evaluation or not evaluation.output_result:
        raise HTTPException(status_code=400, detail="No evaluation result available")

    try:
        ai_response = generate_explanation(
            user_message=request.message,
            evaluation_result=evaluation.output_result
        )
    except Exception as e:
        # Log error and return user-friendly message
        import logging
        logging.error(f"LLM generation failed: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="AI explanation service is temporarily unavailable. Please try again later."
        )

    assistant_reply = ChatMessage(
        session_id=request.session_id,
        role="assistant",
        message=ai_response
    )
    db.add(assistant_reply)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to store message: {str(e)}")

    return {
        "message": "Message stored",
        "ai_response": ai_response
    }


# =========================================
# GET CHAT HISTORY
# =========================================

@router.get("/{evaluation_id}")
def get_chat_sessions(
    evaluation_id: int,
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    evaluation = db.query(Evaluation)\
        .filter(Evaluation.id == evaluation_id)\
        .first()

    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    profile = db.query(Profile)\
        .filter(Profile.id == evaluation.profile_id)\
        .first()

    if profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    sessions = db.query(ChatSession)\
        .filter(ChatSession.evaluation_id == evaluation_id)\
        .all()

    results = []

    for session in sessions:
        messages = db.query(ChatMessage)\
            .filter(ChatMessage.session_id == session.id)\
            .all()

        results.append({
            "session_id": session.id,
            "session_type": session.session_type,
            "panel_name": session.panel_name,
            "messages": [
                {
                    "role": m.role,
                    "message": m.message,
                    "timestamp": m.timestamp
                }
                for m in messages
            ]
        })

    return results
