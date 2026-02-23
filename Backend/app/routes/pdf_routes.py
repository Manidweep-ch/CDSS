from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import tempfile
from typing import Dict, Any

from app.database.session import SessionLocal
from app.auth.security import verify_token
from app.pdf.pdf_extractor import PDFLabExtractor
from app.detection.enhanced_panel_detector import EnhancedPanelDetector

router = APIRouter(prefix="/pdf", tags=["PDF Processing"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================
# UPLOAD & EXTRACT PDF
# =========================================

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user=Depends(verify_token)
):
    """
    Upload PDF lab report and extract test results.
    Returns extracted data and available analyzers.
    """
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Check file size (max 10MB)
    content = await file.read()
    max_size = 10 * 1024 * 1024  # 10MB
    if len(content) > max_size:
        raise HTTPException(status_code=400, detail="File size must be less than 10MB")
    
    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(content)
        tmp_path = tmp_file.name
    
    try:
        # Extract data from PDF
        extracted_data = PDFLabExtractor.extract_from_pdf(tmp_path)
        
        if not extracted_data:
            raise HTTPException(
                status_code=400, 
                detail="No recognizable test results found in PDF"
            )
        
        # Detect available panels
        detection_result = EnhancedPanelDetector.detect_available_panels(extracted_data)
        
        return {
            "success": True,
            "message": f"Extracted {detection_result['total_tests_found']} test results",
            "extracted_data": detection_result["extracted_data"],
            "available_panels": detection_result["available_panels"],
            "panel_details": detection_result["panel_details"],
            "unsupported_tests": detection_result["unsupported_tests"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF processing failed: {str(e)}")
    
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


# =========================================
# EXTRACT FROM TEXT (For Testing)
# =========================================

@router.post("/extract-text")
def extract_from_text(
    text: str,
    current_user=Depends(verify_token)
):
    """
    Extract test results from plain text.
    Useful for testing or manual text input.
    """
    
    extracted_data = PDFLabExtractor.extract_from_text(text)
    
    if not extracted_data:
        raise HTTPException(
            status_code=400,
            detail="No recognizable test results found in text"
        )
    
    detection_result = EnhancedPanelDetector.detect_available_panels(extracted_data)
    
    return {
        "success": True,
        "extracted_data": detection_result["extracted_data"],
        "available_panels": detection_result["available_panels"],
        "panel_details": detection_result["panel_details"],
        "unsupported_tests": detection_result["unsupported_tests"]
    }
