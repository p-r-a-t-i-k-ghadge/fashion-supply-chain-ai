# 🚀 Quick Start Guide

Get your Fashion Supply Chain AI Dashboard running in 5 minutes!

---

## **Step 1: Start the Backend API** (Terminal 1)

```bash
# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Run FastAPI server
uvicorn api.main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

✅ **API is ready!** Access docs at http://127.0.0.1:8000/docs

---

## **Step 2: Initialize Database** (Terminal 2)

```bash
# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Initialize database tables
python db/init_db.py
```

**Expected Output:**
```
Creating database tables in PostgreSQL...
Tables created successfully!!
```

---

## **Step 3: Generate Sample Data** (Terminal 2)

```bash
# Generate 20 products + 6 months of sales/inventory data
python data/generate_synthetic.py
```

**Expected Output:**
```
Generating synthetic dataset for 20 products over 180 days...
Successfully generated database records!
-> 20 products generated.
-> 3600 days of sales and inventory timelines simulated.
-> Mock social media posts initialized.
```

---

## **Step 4: Start the Dashboard** (Terminal 3)

```bash
# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Run Streamlit dashboard
streamlit run dashboard/app.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

✅ **Dashboard is live!** Open http://localhost:8501

---

## **Step 5: Explore the Dashboard**

### **Overview Tab** 📊
- See portfolio summary: 20 products, 5 categories
- Check average price and catalog value
- Review category distribution pie chart

### **Product Analysis Tab** 🔍
- **Try it**: Select any product from dropdown
- **See**: Risk level, current stock, demand forecast
- **Review**: 14-day trend chart with stock projections

### **Product Comparison Tab** ⚖️
- **Try it**: Select 3-5 products for side-by-side analysis
- **Compare**: Price, stock, risk, and forecast metrics
- **Analyze**: Positioning scatter plot

### **Insights Tab** 💡
- **Check**: Critical alerts for high-risk products
- **Review**: Smart recommendations
- **Plan**: Restock priorities based on risk

---

## **🎯 Key Features Explained**

### **Risk Prediction (XGBoost)**
- 🟢 **Low Risk**: Healthy inventory levels → Monitor normally
- 🟡 **Medium Risk**: Approaching reorder point → Prepare orders
- 🔴 **High Risk**: Below reorder point → Restock immediately

### **Demand Forecast (LSTM)**
- Predicts next 24 hours of expected demand
- Based on 180 days of historical sales patterns
- Helps plan inventory and staffing

### **Portfolio Overview**
- Quick view of entire product catalog
- Risk distribution across portfolio
- Identifies problem areas instantly

---

## **📊 Sample Data Breakdown**

When you generate synthetic data:
- **20 Products** across 5 categories:
  - Tops, Bottoms, Outerwear, Footwear, Accessories
- **180 Days** of historical data:
  - Daily sales transactions
  - Inventory levels
  - Reorder events
- **Social Posts**:
  - Mock Twitter/Instagram/TikTok posts
  - Sentiment analysis ready

---

## **🔗 API Endpoints Reference**

Check these endpoints in the API docs: http://127.0.0.1:8000/docs

**Popular endpoints:**
```
Get all products
GET http://127.0.0.1:8000/api/v1/products

Get risk prediction
GET http://127.0.0.1:8000/api/v1/predict/risk/1

Get demand forecast  
GET http://127.0.0.1:8000/api/v1/predict/demand/1

Get portfolio risk summary
GET http://127.0.0.1:8000/api/v1/analytics/risk-summary

Get restock recommendations
GET http://127.0.0.1:8000/api/v1/recommend/restock
```

---

## **⚡ Commands Cheat Sheet**

```bash
# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Start API (Terminal 1)
uvicorn api.main:app --reload

# Initialize DB (Terminal 2)  
python db/init_db.py

# Generate data (Terminal 2)
python data/generate_synthetic.py

# Start Dashboard (Terminal 3)
streamlit run dashboard/app.py

# Install missing packages
pip install -r requirements.txt

# Clear cache
streamlit cache clear
```

---

## **🐛 Troubleshooting**

### **Dashboard shows "Connection disconnected"**
```bash
# Make sure API is running in another terminal
uvicorn api.main:app --reload
```

### **"No module named 'plotly'"**
```bash
# Install missing dependencies
pip install -r requirements.txt
```

### **Database not found error**
```bash
# Initialize database
python db/init_db.py

# Then generate sample data
python data/generate_synthetic.py
```

### **Slow dashboard loading**
```bash
# Clear Streamlit cache
streamlit cache clear

# Restart dashboard
streamlit run dashboard/app.py
```

---

## **🎓 What's Inside**

```
📦 Fashion Supply Chain AI
├── 🎨 dashboard/
│   └── app.py (Streamlit UI - 500+ lines)
├── 🔌 api/
│   ├── main.py (FastAPI server)
│   ├── routes/products.py (Enhanced endpoints)
│   └── schemas.py (Data models)
├── 💾 db/
│   ├── models.py (Database schema)
│   ├── database.py (DB connection)
│   └── init_db.py (Setup script)
├── 📊 data/
│   ├── generate_synthetic.py (Sample data creator)
│   ├── preprocessing.py (Data cleaning)
│   └── raw/ & processed/ (Data folders)
├── 🤖 models/
│   ├── risk/xgboost_model.py (Risk prediction)
│   ├── forecasting/lstm_model.py (Demand forecast)
│   └── nlp/bert_model.py (Sentiment analysis)
└── 📋 requirements.txt (Dependencies)
```

---

## **✨ What's New**

### **Enhanced Dashboard**
✅ Multi-tab interface (Overview, Analysis, Comparison, Insights)
✅ Dynamic date range filtering
✅ Multi-product comparison
✅ Smart recommendations
✅ Professional styling
✅ Better error handling

### **Improved API**
✅ Advanced search and filtering
✅ Analytics endpoints
✅ Sentiment analysis API
✅ Restock recommendations
✅ Better documentation

### **User Features**
✅ Data generation with permission prompt
✅ Category filtering
✅ Risk-based alerts
✅ Downloadable data
✅ Shareable links

---

## **📤 Next: Share Your Dashboard**

Once everything works locally, **deploy to the cloud!**

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- ☁️ Streamlit Cloud deployment
- 🚂 Railway API hosting  
- 🐳 Docker containerization
- 🚀 Full stack deployment

---

## **📚 Learn More**

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Streamlit Docs**: https://docs.streamlit.io
- **SQLAlchemy ORM**: https://docs.sqlalchemy.org
- **XGBoost**: https://xgboost.readthedocs.io
- **LSTM**: https://pytorch.org/docs

---

**🎉 You're all set! Enjoy your Supply Chain AI Dashboard!**

Have questions? Check **DASHBOARD_GUIDE.md** for detailed feature explanations.