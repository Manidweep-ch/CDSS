import pdfplumber
import re
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class PDFLabExtractor:
    """
    Extracts lab test results from medical PDF reports.
    Uses pattern matching to identify biomarkers and their values.
    """

    # Biomarker patterns with common variations
    BIOMARKER_PATTERNS = {
        # Diabetes markers
        "fasting_glucose_level": [
            r"fasting\s+glucose[:\s]+(\d+\.?\d*)",
            r"fbs[:\s]+(\d+\.?\d*)",
            r"glucose\s+fasting[:\s]+(\d+\.?\d*)",
        ],
        "HbA1c_level": [
            r"hba1c[:\s]+(\d+\.?\d*)",
            r"glycated\s+hemoglobin[:\s]+(\d+\.?\d*)",
            r"hemoglobin\s+a1c[:\s]+(\d+\.?\d*)",
        ],
        
        # Cardiovascular markers
        "totChol": [
            r"total\s+cholesterol[:\s]+(\d+\.?\d*)",
            r"cholesterol\s+total[:\s]+(\d+\.?\d*)",
            r"t\.?\s*chol[:\s]+(\d+\.?\d*)",
        ],
        "hdl": [
            r"hdl[:\s]+(\d+\.?\d*)",
            r"hdl\s+cholesterol[:\s]+(\d+\.?\d*)",
        ],
        "ldl": [
            r"ldl[:\s]+(\d+\.?\d*)",
            r"ldl\s+cholesterol[:\s]+(\d+\.?\d*)",
        ],
        "triglycerides": [
            r"triglycerides?[:\s]+(\d+\.?\d*)",
            r"trig[:\s]+(\d+\.?\d*)",
        ],
        "sysBP": [
            r"systolic\s+bp[:\s]+(\d+\.?\d*)",
            r"bp\s+systolic[:\s]+(\d+\.?\d*)",
            r"sbp[:\s]+(\d+\.?\d*)",
        ],
        "diaBP": [
            r"diastolic\s+bp[:\s]+(\d+\.?\d*)",
            r"bp\s+diastolic[:\s]+(\d+\.?\d*)",
            r"dbp[:\s]+(\d+\.?\d*)",
        ],
        
        # Kidney markers
        "serum_creatinine": [
            r"serum\s+creatinine[:\s]+(\d+\.?\d*)",
            r"creatinine[:\s]+(\d+\.?\d*)",
            r"s\.?\s*creat[:\s]+(\d+\.?\d*)",
        ],
        "blood_urea": [
            r"blood\s+urea[:\s]+(\d+\.?\d*)",
            r"bun[:\s]+(\d+\.?\d*)",
        ],
        "gfr": [
            r"egfr[:\s]+(\d+\.?\d*)",
            r"gfr[:\s]+(\d+\.?\d*)",
        ],
        
        # Demographics
        "age": [
            r"age[:\s]+(\d+)",
            r"patient\s+age[:\s]+(\d+)",
        ],
        "sex": [
            r"sex[:\s]+(male|female|m|f)",
            r"gender[:\s]+(male|female|m|f)",
        ],
    }

    @staticmethod
    def extract_from_pdf(pdf_path: str) -> Dict[str, Any]:
        """
        Extract lab values from PDF report.
        Returns dict with biomarker names as keys and numeric values.
        """
        extracted_data = {}
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                
                # Extract text from all pages
                for page in pdf.pages:
                    full_text += page.extract_text() + "\n"
                
                # Normalize text
                full_text = full_text.lower()
                
                # Extract each biomarker
                for biomarker, patterns in PDFLabExtractor.BIOMARKER_PATTERNS.items():
                    for pattern in patterns:
                        match = re.search(pattern, full_text, re.IGNORECASE)
                        if match:
                            value = match.group(1)
                            
                            # Handle sex conversion
                            if biomarker == "sex":
                                if value.lower() in ["male", "m"]:
                                    extracted_data[biomarker] = 1
                                elif value.lower() in ["female", "f"]:
                                    extracted_data[biomarker] = 0
                            else:
                                try:
                                    extracted_data[biomarker] = float(value)
                                except ValueError:
                                    logger.warning(f"Could not convert {value} to float for {biomarker}")
                            
                            break  # Found match, move to next biomarker
                
                logger.info(f"Extracted {len(extracted_data)} biomarkers from PDF")
                return extracted_data
                
        except Exception as e:
            logger.error(f"PDF extraction failed: {str(e)}")
            raise ValueError(f"Failed to extract data from PDF: {str(e)}")

    @staticmethod
    def extract_from_text(text: str) -> Dict[str, Any]:
        """
        Extract lab values from plain text (for testing or manual input).
        """
        extracted_data = {}
        text = text.lower()
        
        for biomarker, patterns in PDFLabExtractor.BIOMARKER_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    value = match.group(1)
                    
                    if biomarker == "sex":
                        if value.lower() in ["male", "m"]:
                            extracted_data[biomarker] = 1
                        elif value.lower() in ["female", "f"]:
                            extracted_data[biomarker] = 0
                    else:
                        try:
                            extracted_data[biomarker] = float(value)
                        except ValueError:
                            pass
                    break
        
        return extracted_data
