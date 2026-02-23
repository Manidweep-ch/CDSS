# 🚀 Quick Start Guide

## First Time Setup (5 minutes)

### 1. Install Prerequisites
- Python 3.8+: https://www.python.org/downloads/
- Node.js 16+: https://nodejs.org/

### 2. Get Groq API Key
1. Go to https://console.groq.com/keys
2. Sign up / Log in
3. Create new API key
4. Copy the key

### 3. Setup Backend
```bash
cd Backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
copy .env.example .env
# Edit .env and paste your Groq API key
```

### 4. Setup Frontend
```bash
cd Frontend
npm install
```

## Running the App (2 commands)

### Terminal 1 - Backend
```bash
cd Backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### Terminal 2 - Frontend
```bash
cd Frontend
npm run dev
```

### Access
- Open browser: http://localhost:5173
- API Docs: http://localhost:8000/docs

## Quick Test

1. Register account
2. Create profile (name, age, gender)
3. Upload PDF from `Backend/sample_pdfs/sample_03_diabetes_confirmed.pdf`
4. Click "Analyze All"
5. View results and chat with AI

## Common Commands

### Backend
```bash
# Activate environment
venv\Scripts\activate

# Run server
uvicorn app.main:app --reload

# Install new package
pip install package_name
pip freeze > requirements.txt

# Run training script
python ml_train/train_diabetes_model.py
```

### Frontend
```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Install new package
npm install package-name
```

## File Structure Quick Reference

```
CDSS/
├── Backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── auth/                # Login/register
│   │   ├── ml/                  # ML predictors
│   │   ├── Rules/               # Clinical rules
│   │   ├── Services/            # Hybrid logic
│   │   └── routes/              # API endpoints
│   ├── models/                  # Trained ML models
│   ├── ml_train/                # Training scripts
│   └── .env                     # API keys (create this!)
│
└── Frontend/
    └── src/
        ├── pages/               # Page components
        ├── components/          # Reusable components
        └── api/                 # API client

```

## Troubleshooting

### Backend won't start
- Check virtual environment is activated
- Verify all packages installed: `pip install -r requirements.txt`
- Check .env file exists with GROQAI_API_KEY

### Frontend won't start
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Clear npm cache: `npm cache clean --force`

### Can't connect to backend
- Verify backend is running on port 8000
- Check browser console for errors
- Verify CORS settings in backend

### PDF upload fails
- Check file is actually a PDF
- Verify file size < 10MB
- Try a sample PDF from Backend/sample_pdfs/

## Next Steps

1. Read INTERNAL_DOCUMENTATION.md for complete details
2. Explore sample PDFs in Backend/sample_pdfs/
3. Check API documentation at http://localhost:8000/docs
4. Modify and experiment with the code!

## Need Help?

- Check INTERNAL_DOCUMENTATION.md
- Review code comments
- Open GitHub issue
- Contact team members

---

Happy coding! 🎉
