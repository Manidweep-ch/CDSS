from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any

from app.detection.panel_detector import detect_panels
from app.master_service import CDSSMasterRouter

from app.database.base import Base
from app.database.engine import engine
import app.models.user
import app.models.profile
import app.models.evaluation
import app.models.chat_session
import app.models.chat_message
from app.auth.routes import router as auth_router
from app.auth.security import verify_token
from app.routes.profile_routes import router as profile_router
from app.routes.evaluation_routes import router as evaluation_router
from app.routes.chat_routes import router as chat_router
from app.routes.pdf_routes import router as pdf_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Hybrid Multi-Panel CDSS")

# CORS configuration - supports both development and production
import os
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(evaluation_router)
app.include_router(chat_router)
app.include_router(pdf_router)
security = HTTPBearer()


# ======================================
# MOCK JWT VALIDATION (Replace Later)
# ======================================

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    # ⚠ Replace with real JWT validation
    if not token or token != "test-token":
        raise HTTPException(status_code=403, detail="Invalid or missing token")

    return {"user_id": 1}


# ======================================
# HEALTH CHECK
# ======================================

@app.get("/health")
def health():
    return {"status": "CDSS Operational"}


# ======================================
# PANEL DETECTION
# ======================================

@app.post("/detect")
def detect(data: Dict[str, Any], user=Depends(verify_token)):
    return detect_panels(data)


# ======================================
# SINGLE PANEL EVALUATION
# ======================================

@app.post("/evaluate")
def evaluate(panel: str, data: Dict[str, Any], user=Depends(verify_token)):
    try:
        return CDSSMasterRouter.route_single(panel, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ======================================
# MULTIPLE PANEL EVALUATION
# ======================================

@app.post("/evaluate-multiple")
def evaluate_multiple(panels: List[str], data: Dict[str, Any], user=Depends(verify_token)):
    return CDSSMasterRouter.route_multiple(panels, data)
