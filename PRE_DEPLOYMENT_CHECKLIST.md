# ✅ Pre-Deployment Checklist

Complete this checklist before deploying to ensure smooth deployment.

## 1. Code Preparation

### Backend
- [ ] All dependencies in `requirements.txt`
- [ ] `.env.example` file exists with all required variables
- [ ] Database engine supports PostgreSQL
- [ ] CORS settings use environment variable
- [ ] No hardcoded URLs or secrets
- [ ] Health check endpoint exists (`/health`)
- [ ] All imports work correctly

### Frontend
- [ ] `VITE_API_URL` uses environment variable
- [ ] Build command works: `npm run build`
- [ ] No console.log statements in production code
- [ ] All routes work correctly
- [ ] Error boundaries implemented
- [ ] Loading states for API calls

## 2. Environment Variables

### Backend (.env)
- [ ] `GROQAI_API_KEY` - Get from console.groq.com
- [ ] `SECRET_KEY` - Generate random string (32+ chars)
- [ ] `DATABASE_URL` - Will be provided by Render
- [ ] `ALLOWED_ORIGINS` - Frontend URL

### Frontend (.env)
- [ ] `VITE_API_URL` - Backend URL

## 3. GitHub Setup

- [ ] GitHub account created
- [ ] Repository created (public or private)
- [ ] `.gitignore` file in place
- [ ] All sensitive files excluded (.env, __pycache__, node_modules)
- [ ] README.md is complete
- [ ] Code is committed and pushed

## 4. External Services

- [ ] Groq API account created
- [ ] Groq API key obtained
- [ ] API key has sufficient credits
- [ ] Tested API key locally

## 5. Testing

### Local Testing
- [ ] Backend runs without errors
- [ ] Frontend builds successfully
- [ ] Can register new user
- [ ] Can login
- [ ] Can create profile
- [ ] Can upload PDF
- [ ] Can run analysis
- [ ] Chatbot works
- [ ] History page loads

### Production Build Testing
```bash
# Test backend
cd Backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test frontend production build
cd Frontend
npm run build
npm run preview
```

- [ ] Production build works locally
- [ ] No console errors
- [ ] All features work in production build

## 6. Documentation

- [ ] README.md is complete
- [ ] DEPLOYMENT_GUIDE.md reviewed
- [ ] Environment variables documented
- [ ] API endpoints documented

## 7. Security

- [ ] No API keys in code
- [ ] No passwords in code
- [ ] `.env` in `.gitignore`
- [ ] Strong SECRET_KEY generated
- [ ] CORS properly configured
- [ ] SQL injection protection (SQLAlchemy handles this)

## 8. Performance

- [ ] Large files excluded from Git (models are OK if <100MB)
- [ ] Unnecessary dependencies removed
- [ ] Database queries optimized
- [ ] Frontend bundle size reasonable

## 9. Deployment Platform

### Render Account
- [ ] Account created at render.com
- [ ] GitHub connected
- [ ] Payment method added (optional, for paid tier)

### Alternative: Railway
- [ ] Account created at railway.app
- [ ] GitHub connected

## 10. Post-Deployment

- [ ] Backend URL noted
- [ ] Frontend URL noted
- [ ] Environment variables updated with actual URLs
- [ ] CORS settings updated
- [ ] Tested deployed application
- [ ] All features work in production
- [ ] Logs checked for errors

---

## Quick Commands Reference

### Generate SECRET_KEY
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Test Backend Locally
```bash
cd Backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

### Test Frontend Build
```bash
cd Frontend
npm run build
npm run preview
```

### Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

---

## Common Issues Before Deployment

### Issue: Build fails locally
**Fix**: 
- Check all dependencies installed
- Run `pip install -r requirements.txt`
- Run `npm install`

### Issue: Environment variables not loading
**Fix**:
- Check `.env` file exists
- Check variable names match code
- Restart server after changing .env

### Issue: Database errors
**Fix**:
- Delete `cdss.db` and restart (development only)
- Check SQLAlchemy models are correct

### Issue: CORS errors
**Fix**:
- Check ALLOWED_ORIGINS includes frontend URL
- Check frontend is using correct backend URL

---

## Ready to Deploy?

If all checkboxes are checked, you're ready to deploy!

Follow the **DEPLOYMENT_GUIDE.md** for step-by-step instructions.

---

## Deployment Timeline

- **GitHub Setup**: 10 minutes
- **Render Backend Setup**: 15 minutes
- **Render Frontend Setup**: 10 minutes
- **Testing**: 15 minutes
- **Total**: ~50 minutes

---

**Good luck with your deployment! 🚀**
