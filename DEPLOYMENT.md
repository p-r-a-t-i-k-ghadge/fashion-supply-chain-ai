# 🚀 Deployment Guide - Fashion Supply Chain AI Dashboard

This guide walks you through deploying your dashboard to the cloud for public access.

---

## 📋 Prerequisites

- GitHub account (for storing your code)
- Streamlit Cloud account (free tier available)
- Railway or Vercel account (for API backend)

---

## **Option 1: Streamlit Cloud (FASTEST - Dashboard Only)**

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: Fashion Supply Chain AI Dashboard"
git remote add origin https://github.com/YOUR_USERNAME/fashion-supply-chain-ai.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Click "New App"
3. Connect your GitHub repository
4. Select the branch and `dashboard/app.py` as the main file
5. Click "Deploy"

**Live in 2 minutes!**

---

## **Option 2: Full Stack Deployment (API + Dashboard)**

### **A. Deploy API Backend on Railway**

1. **Create Railway Account**: https://railway.app

2. **Create `.env` file** (add to `.gitignore`):
```env
DATABASE_URL=sqlite:///./fashion_supply.db
FASTAPI_ENV=production
```

3. **Create `requirements.txt`** (if not present):
```bash
pip freeze > requirements.txt
```

4. **Create `Procfile`**:
```
web: uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

5. **Deploy to Railway**:
   - Connect GitHub repo
   - Railway auto-detects Python project
   - Set PORT environment variable (Railway does this automatically)
   - API available at: `https://your-app.railway.app`

### **B. Deploy Dashboard on Streamlit Cloud**

1. **Update API URL** in `dashboard/app.py`:
```python
# Change from:
API_BASE_URL = "http://127.0.0.1:8000/api/v1"

# To:
API_BASE_URL = "https://your-api.railway.app/api/v1"
```

2. **Push changes**:
```bash
git add .
git commit -m "Update API URL for production"
git push
```

3. **Deploy same way as Option 1**

---

## **Option 3: Docker Deployment (Full Control)**

### **A. Create Dockerfile**
```dockerfile
FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000 8501

# Start both services
CMD sh -c "uvicorn api.main:app --host 0.0.0.0 --port 8000 & streamlit run dashboard/app.py --server.port=8501 --server.address=0.0.0.0"
```

### **B. Create docker-compose.yml**
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
      - "8501:8501"
    environment:
      - DATABASE_URL=sqlite:///./fashion_supply.db
```

### **C. Run Locally**
```bash
docker-compose up
```

### **D. Deploy to Docker Hub / AWS ECR**
```bash
docker build -t your-username/fashion-supply-chain .
docker push your-username/fashion-supply-chain
```

---

## **Option 4: Heroku Deployment**

1. **Create Heroku Account**: https://heroku.com

2. **Create Procfile**:
```
web: uvicorn api.main:app --host 0.0.0.0 --port $PORT
worker: streamlit run dashboard/app.py --server.port $PORT
```

3. **Deploy**:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

---

## **Option 5: Google Cloud Run (Serverless)**

### **Step 1: Create Deployment Script** (`deploy.sh`):
```bash
#!/bin/bash

PROJECT_ID="your-project-id"
SERVICE_NAME="fashion-supply-chain"
REGION="us-central1"

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy API
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated
```

### **Step 2: Run Deployment**:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## **Quick Reference: Sharing Links**

Once deployed:

### **Share Dashboard Link:**
```
https://your-streamlit-app.streamlit.app
```

### **Share API Documentation:**
```
https://your-api.railway.app/docs
```

### **Share API Endpoints:**
```
Base URL: https://your-api.railway.app/api/v1

Available Endpoints:
- GET /products - List all products
- GET /products/{id} - Get product details
- GET /predict/risk/{id} - Get risk prediction
- GET /predict/demand/{id} - Get demand forecast
- GET /analytics/risk-summary - Portfolio risk analysis
- GET /analytics/sentiment - Brand sentiment
- GET /recommend/restock - Restock recommendations
```

---

## **Environment Variables (for Production)**

Create `.streamlit/secrets.toml` for Streamlit Cloud:

```toml
API_BASE_URL = "https://your-api.railway.app/api/v1"
DATABASE_URL = "your-production-db-url"
```

---

## **Troubleshooting**

### **Issue: 404 API Not Found**
- ✅ Check API URL is correct
- ✅ Ensure FastAPI is running
- ✅ Check CORS settings in `api/main.py`

### **Issue: Database Not Found**
- ✅ Run `python db/init_db.py` before deploying
- ✅ Use cloud database (PostgreSQL on Railway)
- ✅ Ensure write permissions

### **Issue: Slow Performance**
- ✅ Enable caching in Streamlit
- ✅ Use CDN for static files
- ✅ Optimize database queries with indexes

---

## **Next Steps**

1. ✅ **Deploy**: Choose an option above
2. ✅ **Test**: Visit both URLs
3. ✅ **Monitor**: Set up logging
4. ✅ **Share**: Distribute links to stakeholders
5. ✅ **Iterate**: Collect feedback and improve

---

## **Security Checklist**

- [ ] Add authentication to API
- [ ] Use HTTPS only
- [ ] Hide sensitive data in environment variables
- [ ] Enable CORS only for trusted domains
- [ ] Set rate limiting
- [ ] Add API key authentication

---

## **Support**

- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-cloud
- **FastAPI Docs**: https://fastapi.tiangolo.com/deployment/
- **Railway Docs**: https://railway.app/docs

---

**Happy Deploying! 🚀**