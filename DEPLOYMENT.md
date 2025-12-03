# Deployment Guide

## Project Structure

```
GENAI_PROJ/
├── app/                    # Backend (FastAPI)
├── models/                 # ML models
├── frontend/               # Frontend for Vercel
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── vercel.json
├── render.yaml             # Render config
├── Procfile               # Render process file
├── runtime.txt            # Python version
└── requirements.txt       # Dependencies
```

---

## 1. Deploy Backend to Render

### Option A: Using Render Dashboard

1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `email-classifier-api`
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"
     ```
   - **Start Command**: 
     ```
     uvicorn app.fastapi_app:app --host 0.0.0.0 --port $PORT
     ```
5. Click **"Create Web Service"**
6. Wait for deployment (5-10 minutes)
7. Copy your URL: `https://your-app-name.onrender.com`

### Option B: Using render.yaml (Blueprint)

1. Push your code to GitHub
2. Go to Render Dashboard → **"Blueprints"**
3. Connect your repo - Render will auto-detect `render.yaml`
4. Deploy!

---

## 2. Deploy Frontend to Vercel

### Step 1: Update API URL

Edit `frontend/script.js` and update line 7:

```javascript
const API_BASE_URL = 'https://your-render-app-name.onrender.com';
```

Replace `your-render-app-name` with your actual Render URL.

### Step 2: Deploy to Vercel

#### Option A: Using Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend folder
cd frontend

# Deploy
vercel

# Follow prompts, then for production:
vercel --prod
```

#### Option B: Using Vercel Dashboard

1. Go to [vercel.com](https://vercel.com) and sign up/login
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: `Other`
5. Click **"Deploy"**

---

## 3. Test Your Deployment

1. **Backend Health Check**: Visit `https://your-render-app.onrender.com/api/health`
2. **API Docs**: Visit `https://your-render-app.onrender.com/docs`
3. **Frontend**: Visit your Vercel URL

---

## Environment Variables (Optional)

### Render
No environment variables required for basic setup.

### Vercel
If you want to use environment variables for the API URL:

1. Add in Vercel Dashboard → Settings → Environment Variables:
   - `VITE_API_URL` = `https://your-render-app.onrender.com`

2. Update `script.js`:
   ```javascript
   const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://your-render-app.onrender.com';
   ```

---

## Troubleshooting

### Render Issues

1. **Build fails**: Check `requirements.txt` has all dependencies
2. **NLTK errors**: Ensure build command downloads NLTK data
3. **Model not found**: Ensure `models/` folder is committed to git

### Vercel Issues

1. **CORS errors**: Backend already has CORS enabled for all origins
2. **API not connecting**: Double-check the API_BASE_URL in script.js

### Common Fixes

```bash
# Make sure models are tracked in git
git add models/*.pkl -f
git commit -m "Add model files"
git push
```

---

## URLs After Deployment

- **Backend API**: `https://your-app.onrender.com`
- **API Docs**: `https://your-app.onrender.com/docs`
- **Frontend**: `https://your-app.vercel.app`
