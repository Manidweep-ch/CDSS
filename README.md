# 🏥 MediCare CDSS - Clinical Decision Support System

An AI-powered Clinical Decision Support System that analyzes medical lab reports and provides risk assessments for Diabetes, Cardiovascular, and Kidney health conditions.

## 🌟 Features

- **PDF Lab Report Analysis**: Upload medical lab reports in PDF format for automatic data extraction
- **Multi-Panel Analysis**: Simultaneous analysis of Diabetes, Cardiovascular, and Kidney health panels
- **Hybrid AI System**: Combines machine learning models with clinical rule-based systems
- **AI Chatbot**: Interactive AI assistant powered by Groq for explaining results
- **Patient Profile Management**: Manage multiple patient profiles with historical data
- **Analysis History**: Track and review past evaluations
- **Dark/Light Theme**: Modern, accessible UI with theme switching

## 🚀 Tech Stack

### Frontend
- **React 19** - UI framework
- **React Router** - Navigation
- **Axios** - HTTP client
- **Material-UI** - Component library
- **Vite** - Build tool

### Backend
- **FastAPI** - Python web framework
- **SQLAlchemy** - ORM for database management
- **XGBoost** - Machine learning models
- **SHAP** - Model explainability
- **Groq AI** - LLM for chatbot
- **PyPDF2 & pdfplumber** - PDF processing
- **JWT** - Authentication

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Groq API Key ([Get one here](https://console.groq.com/keys))

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/medicare-cdss.git
cd medicare-cdss
```

### 2. Backend Setup
```bash
cd Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
copy .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Frontend Setup
```bash
cd Frontend

# Install dependencies
npm install

# The frontend will connect to http://localhost:8000 by default
```

## 🏃 Running the Application

### Start Backend Server
```bash
cd Backend
uvicorn app.main:app --reload --port 8000
```

### Start Frontend Development Server
```bash
cd Frontend
npm run dev
```

Access the application at `http://localhost:5173`

## 📊 Health Panels

### 1. Diabetes Panel
- **Parameters**: HbA1c, FBS (Fasting Blood Sugar), PPBS (Post-Prandial Blood Sugar)
- **Algorithm**: XGBoost with Platt Calibration
- **Features**: 21 clinical features including BMI, age, lifestyle factors

### 2. Cardiovascular Panel
- **Parameters**: Blood Pressure (Systolic/Diastolic), Cholesterol, Heart Rate, BMI
- **Algorithm**: XGBoost with clinical feature engineering
- **Risk Assessment**: 10-year CHD (Coronary Heart Disease) risk

### 3. Kidney Panel
- **Parameters**: Serum Creatinine, Blood Urea (BUN), Age
- **Algorithm**: XGBoost with Standard Scaling
- **Detection**: Chronic Kidney Disease (CKD) classification

## 🔐 Authentication

The system uses JWT-based authentication:
- Register a new account
- Login to receive an access token
- Token is automatically included in API requests

## 📁 Project Structure

```
CDSS/
├── Backend/
│   ├── app/
│   │   ├── auth/          # Authentication logic
│   │   ├── database/      # Database configuration
│   │   ├── detection/     # PDF panel detection
│   │   ├── llm/           # Groq AI chatbot
│   │   ├── ml/            # ML predictors & explainers
│   │   ├── models/        # Database models
│   │   ├── pdf/           # PDF extraction
│   │   ├── routes/        # API endpoints
│   │   ├── Rules/         # Clinical rule engines
│   │   ├── schemas/       # Pydantic schemas
│   │   └── Services/      # Hybrid decision services
│   ├── Data_set/          # Training datasets
│   ├── ml_train/          # Model training scripts
│   ├── models/            # Trained ML models (.pkl)
│   └── sample_pdfs/       # Sample test PDFs
│
└── Frontend/
    └── src/
        ├── api/           # API client
        ├── components/    # React components
        ├── context/       # React context (Auth, Theme)
        └── pages/         # Page components
```

## 🌐 Deployment

This application can be deployed for free on Render. See our comprehensive guides:

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Step-by-step deployment instructions
- **[DEPLOYMENT_OPTIONS.md](DEPLOYMENT_OPTIONS.md)** - Compare different hosting platforms
- **[PRE_DEPLOYMENT_CHECKLIST.md](PRE_DEPLOYMENT_CHECKLIST.md)** - Ensure you're ready to deploy

### Quick Deploy on Render (Recommended)
1. Push your code to GitHub
2. Sign up at [render.com](https://render.com)
3. Create Web Service for Backend
4. Create Static Site for Frontend
5. Add environment variables
6. Deploy! 🚀

Estimated time: 30 minutes | Cost: Free

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This system is designed as a clinical decision support tool and should NOT be used as a replacement for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical decisions.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ for better healthcare
