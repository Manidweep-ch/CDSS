# 🚀 Complete Deployment Guide

## Overview
This guide will help you deploy your MediCare CDSS application to the internet for free using Render.

## Prerequisites
- [x] GitHub account
- [x] Groq API key
- [x] Project code ready

---

## Method 1: Deploy on Render (RECOMMENDED - Free & Easy)

### Step 1: Prepare Your Code

#### 1.1 Update Frontend Environment
Create `Frontend/.env.production`:
```bash
VITE_API_URL=https://medicare-cdss-backend.onrender.com
```
(Replace with your actual backend URL after deployment)

#### 1.2 Test Locally First
```bash
# Backend
cd Backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Frontend (new terminal)
cd Frontend
npm run build
npm run preview
```

### Step 2: Push to GitHub

```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Ready for deployment"

# Create GitHub repo at github.com/new
# Then add remote (replace with your URL)
git remote add origin https://github.com/yourusername/medicare-cdss.git

# Push
git push -u origin main
```

### Step 3: Deploy Backend on Render

1. **Go to Render**: https://render.com
2. **Sign up** with GitHub
3. **Click "New +"** → **"Web Service"**
4. **Connect your GitHub repository**
5. **Configure**:
   - **Name**: `medicare-cdss-backend`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Root Directory**: `Backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

6. **Add Environment Variables**:
   Click "Advanced" → "Add Environment Variable":
   ```
   GROQAI_API_KEY = your_groq_api_key_here
   SECRET_KEY = (click "Generate" button)
   ALLOWED_ORIGINS = https://medicare-cdss-frontend.onrender.com
   ```

7. **Create PostgreSQL Database**:
   - Go to Dashboard → "New +" → "PostgreSQL"
   - Name: `medicare-cdss-db`
   - Plan: Free
   - Click "Create Database"
   - Copy the "Internal Database URL"

8. **Add Database URL to Backend**:
   - Go back to your backend service
   - Environment Variables → Add:
   ```
   DATABASE_URL = (paste the Internal Database URL)
   ```

9. **Click "Create Web Service"**
   - Wait 5-10 minutes for deployment
   - Your backend URL: `https://medicare-cdss-backend.onrender.com`

### Step 4: Deploy Frontend on Render

1. **Click "New +"** → **"Static Site"**
2. **Connect same GitHub repository**
3. **Configure**:
   - **Name**: `medicare-cdss-frontend`
   - **Branch**: `main`
   - **Root Directory**: `Frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

4. **Add Environment Variable**:
   ```
   VITE_API_URL = https://medicare-cdss-backend.onrender.com
   ```
   (Use your actual backend URL from Step 3)

5. **Click "Create Static Site"**
   - Wait 5-10 minutes
   - Your frontend URL: `https://medicare-cdss-frontend.onrender.com`

### Step 5: Update CORS Settings

1. Go to your backend service on Render
2. Update `ALLOWED_ORIGINS` environment variable:
   ```
   ALLOWED_ORIGINS = https://medicare-cdss-frontend.onrender.com
   ```
3. Click "Save Changes" (backend will redeploy)

### Step 6: Test Your Deployment

1. Visit your frontend URL
2. Register a new account
3. Create a profile
4. Upload a sample PDF
5. Run analysis
6. Test chatbot

### 🎉 Done! Your app is live!

---

## Method 2: Deploy on Railway

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy on Railway

1. **Go to Railway**: https://railway.app
2. **Sign up** with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Select your repository**
5. **Add PostgreSQL**:
   - Click "New" → "Database" → "PostgreSQL"
6. **Configure Backend**:
   - Click on your service
   - Settings → Root Directory: `Backend`
   - Settings → Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Variables → Add:
     ```
     GROQAI_API_KEY = your_key
     SECRET_KEY = generate_random_string
     DATABASE_URL = ${{Postgres.DATABASE_URL}}
     ALLOWED_ORIGINS = your_frontend_url
     ```
7. **Configure Frontend**:
   - New → GitHub Repo (same repo)
   - Settings → Root Directory: `Frontend`
   - Settings → Build Command: `npm install && npm run build`
   - Settings → Start Command: `npm run preview`
   - Variables → Add:
     ```
     VITE_API_URL = your_backend_url
     ```

---

## Method 3: Vercel (Frontend) + Render (Backend)

### Frontend on Vercel

1. **Go to Vercel**: https://vercel.com
2. **Import Git Repository**
3. **Configure**:
   - Framework Preset: Vite
   - Root Directory: `Frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. **Environment Variables**:
   ```
   VITE_API_URL = your_backend_url
   ```
5. **Deploy**

### Backend on Render
Follow Method 1, Step 3 above

---

## Post-Deployment Checklist

### Security
- [ ] Changed SECRET_KEY to strong random value
- [ ] Set correct ALLOWED_ORIGINS
- [ ] Groq API key is set
- [ ] Database URL is configured
- [ ] HTTPS is enabled (automatic on Render/Vercel)

### Testing
- [ ] User registration works
- [ ] Login works
- [ ] Profile creation works
- [ ] PDF upload works
- [ ] Analysis runs successfully
- [ ] Chatbot responds
- [ ] History page loads

### Monitoring
- [ ] Check Render logs for errors
- [ ] Test on mobile devices
- [ ] Test on different browsers
- [ ] Monitor Groq API usage

---

## Troubleshooting

### Issue: Backend won't start
**Check**:
- Render logs for error messages
- All environment variables are set
- Database URL is correct
- requirements.txt has all dependencies

### Issue: Frontend can't connect to backend
**Check**:
- VITE_API_URL is correct
- ALLOWED_ORIGINS includes frontend URL
- Backend is running (check Render dashboard)
- CORS settings are correct

### Issue: Database errors
**Check**:
- DATABASE_URL is set correctly
- PostgreSQL database is running
- Tables are created (check logs)

### Issue: Groq API errors
**Check**:
- API key is correct
- API key has credits
- Check Groq API status

### Issue: Free tier limitations
**Render Free Tier**:
- Sleeps after 15 min inactivity
- 750 hours/month limit
- 512 MB RAM
- Shared CPU

**Solutions**:
- Upgrade to paid plan ($7/month)
- Use Railway ($5 free credit/month)
- Keep app awake with UptimeRobot (free)

---

## Keeping Your App Awake (Optional)

Free tier apps sleep after inactivity. To keep them awake:

### Option 1: UptimeRobot
1. Go to https://uptimerobot.com
2. Sign up (free)
3. Add New Monitor:
   - Type: HTTP(s)
   - URL: Your backend health endpoint
   - Interval: 5 minutes
4. This pings your app every 5 minutes to keep it awake

### Option 2: Cron-job.org
1. Go to https://cron-job.org
2. Sign up (free)
3. Create new cron job:
   - URL: Your backend URL
   - Interval: Every 5 minutes

---

## Cost Breakdown

### Free Tier (Recommended for Students)
- **Render**: Free (with limitations)
- **Groq API**: Free tier (limited requests)
- **Total**: $0/month

### Paid Tier (For Production)
- **Render Web Service**: $7/month
- **Render PostgreSQL**: $7/month
- **Groq API**: Pay-as-you-go (~$5-10/month)
- **Total**: ~$20-25/month

---

## Custom Domain (Optional)

### Add Custom Domain on Render
1. Buy domain (Namecheap, GoDaddy, etc.)
2. In Render dashboard → Settings → Custom Domain
3. Add your domain
4. Update DNS records as instructed
5. Wait for SSL certificate (automatic)

---

## Updating Your Deployed App

### Automatic Deployment (Recommended)
Render/Vercel automatically redeploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update: description of changes"
git push origin main

# Render/Vercel will automatically redeploy
```

### Manual Deployment
1. Go to Render dashboard
2. Click on your service
3. Click "Manual Deploy" → "Deploy latest commit"

---

## Monitoring & Logs

### View Logs on Render
1. Go to your service dashboard
2. Click "Logs" tab
3. See real-time logs
4. Filter by error/warning

### Check Database
1. Go to PostgreSQL database
2. Click "Connect"
3. Use provided connection string with pgAdmin or DBeaver

---

## Backup & Recovery

### Database Backup
1. Render automatically backs up PostgreSQL
2. Manual backup:
   - Dashboard → Database → "Backups"
   - Click "Create Backup"

### Code Backup
- Your code is on GitHub (already backed up)
- Download from GitHub anytime

---

## Next Steps After Deployment

1. **Share your app**:
   - Add URL to your resume
   - Share with friends/professors
   - Post on LinkedIn

2. **Monitor usage**:
   - Check Render dashboard
   - Monitor Groq API usage
   - Review logs regularly

3. **Gather feedback**:
   - Ask users to test
   - Fix bugs
   - Add features

4. **Improve**:
   - Add more health panels
   - Improve UI/UX
   - Optimize performance

---

## Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Your Team**: Check INTERNAL_DOCUMENTATION.md

---

**Congratulations on deploying your first full-stack application! 🎉**
