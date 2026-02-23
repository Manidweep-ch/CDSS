from groq import Groq
import os
from dotenv import load_dotenv
import json
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Validate API key on module load
GROQ_API_KEY = os.getenv("GROQAI_API_KEY")
if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
    logger.warning("GROQAI_API_KEY not configured. Chat functionality will be limited.")
    client = None
else:
    client = Groq(api_key=GROQ_API_KEY)

def generate_explanation(user_message: str, evaluation_result: dict):
    """
    Generate AI explanation for evaluation results.
    Raises exception if API key not configured or API call fails.
    """
    
    if not client:
        raise ValueError("GROQAI_API_KEY not configured. Please set it in .env file.")

    system_prompt = """
You are a clinical explanation assistant.
You must ONLY explain the provided structured evaluation result.
You must NOT give new diagnoses.
You must NOT override decisions.
You must NOT invent medical advice.
Explain clearly in patient-friendly language.
Be calm, structured and factual.
    """

    context = f"""
Stored Clinical Evaluation Result:
{json.dumps(evaluation_result, indent=2)}

User Question:
{user_message}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context}
            ],
            temperature=0.3,
            max_tokens=700,
            timeout=30  # 30 second timeout
        )

        return completion.choices[0].message.content
    
    except Exception as e:
        logger.error(f"Groq API call failed: {str(e)}")
        raise RuntimeError(f"Failed to generate explanation: {str(e)}")
