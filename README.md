# 📦 Fashion Supply Chain AI Dashboard

A **professional-grade, AI-powered supply chain management system** for fashion retailers. Combines machine learning models for demand forecasting, risk prediction, and brand sentiment analysis with an intuitive interactive dashboard.

---

## ✨ What's Inside

### **🎨 Interactive Dashboard** (Streamlit)
- **4 Professional Tabs**: Overview, Product Analysis, Comparison, Insights
- **Real-time Analytics**: Risk scores, demand forecasts, sentiment analysis
- **Multi-product Comparison**: Side-by-side analysis of multiple SKUs
- **Smart Recommendations**: AI-powered inventory insights
- **Beautiful Visualizations**: Plotly charts and metrics

### **🔌 REST API** (FastAPI)
- **15+ Endpoints**: Products, predictions, analytics, recommendations
- **Advanced Filtering**: Search by category, SKU, and more
- **ML Integration**: XGBoost risk scoring, LSTM demand forecasting
- **Auto Documentation**: Swagger UI at `/docs`

### **🤖 ML Models**
- **LSTM**: 24-hour demand forecasting (PyTorch)
- **XGBoost**: Inventory risk classification
- **BERT**: Brand sentiment analysis from social media (HuggingFace)

### **💾 Database**
- **SQLAlchemy ORM**: Clean database abstraction
- **SQLite (Dev) / PostgreSQL (Prod)**: Flexible deployment
- **Comprehensive Schema**: Products, Sales, Inventory, Forecasts, Risks

---

## 🚀 Quick Start (5 minutes)

### **Prerequisites**
- Python 3.11+
- Git
- Virtual environment (recommended)

### **Step 1: Clone & Setup**
```bash
# Clone repository
git clone <your-repo-url>
cd fashion_supply_chain_using_ai

# Create virtual environment
python -m venv venv
& ".\venv\Scripts\Activate.ps1"  # Windows
source venv/bin/activate         # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### **Step 2: Initialize Database**
```bash
python db/init_db.py
python data/generate_synthetic.py
```

### **Step 3: Run the System**

**Terminal 1 - API Server:**
```bash
uvicorn api.main:app --reload
# 🌐 API: http://127.0.0.1:8000
# 📚 Docs: http://127.0.0.1:8000/docs
```

**Terminal 2 - Dashboard:**
```bash
streamlit run dashboard/app.py
# 📊 Dashboard: http://localhost:8501
```

✅ **Complete!** Both services running.

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[QUICKSTART.md](QUICKSTART.md)** | 5-minute setup guide with commands |
| **[DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md)** | Feature explanations & how-to guides |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Cloud deployment (5 options) |
| **[CONFIGURATION.md](CONFIGURATION.md)** | Environment setup & security |
| **[BEST_PRACTICES.md](BEST_PRACTICES.md)** | Analysis strategies & tips |
| **[IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md)** | What's new in v2 |

---

## 📊 Dashboard Features

### **Tab 1: Overview** 📊
Portfolio summary with category distribution and KPIs
```
✅ Total products: 20
✅ Categories: 5
✅ Avg price: $84.99
✅ Total catalog value: $1,699.80
```

### **Tab 2: Product Analysis** 🔍
Deep dive into single products with risk, stock, and demand
```
✅ Risk assessment (Low/Medium/High)
✅ Current stock levels
✅ 24-hour demand forecast
✅ 14-day trend projection
✅ Action recommendations
```

### **Tab 3: Product Comparison** ⚖️
Compare 2-10 products side-by-side
```
✅ Comparison table
✅ Price vs. stock visualization
✅ Risk distribution
✅ Performance metrics
```

### **Tab 4: Insights & Recommendations** 💡
Portfolio-level analysis and smart actions
```
✅ Critical alerts
✅ Risk distribution chart
✅ Smart recommendations
✅ Restock priorities
```

---

## 🔌 API Endpoints

### **Products**
```bash
GET  /api/v1/products              # List all products
GET  /api/v1/products/{id}         # Product details
GET  /api/v1/categories             # Available categories
```

### **Predictions**
```bash
GET  /api/v1/predict/risk/{id}     # Risk score (XGBoost)
GET  /api/v1/predict/demand/{id}   # Demand forecast (LSTM)
```

### **Analytics**
```bash
GET  /api/v1/analytics/risk-summary      # Portfolio risk overview
GET  /api/v1/analytics/sentiment          # Brand sentiment analysis
GET  /api/v1/recommend/restock            # Restock recommendations
```

**Full Documentation**: http://127.0.0.1:8000/docs

---

## 📁 Project Structure

```
📦 fashion_supply_chain_using_ai/
├── 🎨 dashboard/
│   └── app.py              (Streamlit UI - 800+ lines)
├── 🔌 api/
│   ├── main.py             (FastAPI server)
│   ├── routes/products.py  (API endpoints)
│   └── schemas.py          (Pydantic models)
├── 💾 db/
│   ├── models.py           (SQLAlchemy ORM)
│   ├── database.py         (DB connection)
│   └── init_db.py          (Setup script)
├── 📊 data/
│   ├── generate_synthetic.py (Sample data)
│   └── preprocessing.py    (Data pipeline)
├── 🤖 models/
│   ├── risk/xgboost_model.py        (Risk prediction)
│   ├── forecasting/lstm_model.py    (Demand forecast)
│   └── nlp/bert_model.py            (Sentiment analysis)
├── 📝 requirements.txt
├── 📖 README.md            (You are here!)
└── 📚 Documentation files  (QUICKSTART, DEPLOYMENT, etc.)
```

---

## ⚙️ System Architecture

```
┌─────────────────────────────────────────┐
│     📊 Streamlit Dashboard (Port 8501)  │
│  [Overview] [Analysis] [Compare] [AI]   │
└────────────────┬────────────────────────┘
                 │ HTTP Requests
┌────────────────▼────────────────────────┐
│    🔌 FastAPI Server (Port 8000)        │
│  /api/v1/ {products, risk, demand...}   │
└────────────────┬────────────────────────┘
                 │ SQL Queries
┌────────────────▼────────────────────────┐
│     💾 SQLite/PostgreSQL Database       │
│  [Products] [Inventory] [Sales] [Risk]  │
└─────────────────────────────────────────┘
```

---

## 🤖 Machine Learning Models

### **LSTM (Demand Forecasting)**
- **Libraries**: PyTorch
- **Task**: 24-hour demand prediction
- **Input**: 180 days historical sales
- **Output**: Next-day quantity forecast

### **XGBoost (Risk Classification)**
- **Libraries**: scikit-learn, joblib
- **Task**: Inventory risk assessment
- **Input**: Stock level, reorder point, lead time
- **Output**: Risk level (Low/Medium/High)

### **BERT (Sentiment Analysis)**
- **Libraries**: HuggingFace Transformers
- **Task**: Brand sentiment from social posts
- **Input**: Twitter, Instagram, TikTok posts
- **Output**: Sentiment score (0.0 - 1.0)

---

## 📊 Sample Data

When you generate synthetic data:
- **20 Products** across 5 categories (Tops, Bottoms, Outerwear, Footwear, Accessories)
- **180 Days** of historical sales and inventory data
- **3,600 Records** of daily inventory transactions
- **240 Social Posts** for sentiment analysis

---

## 🚀 Deployment Options

Choose your preferred deployment method:

### **Option 1: Streamlit Cloud** (Easiest) ⭐
- Deploy dashboard in 2 minutes
- Free tier available
- See [DEPLOYMENT.md](DEPLOYMENT.md)

### **Option 2: Railway + Streamlit Cloud**
- Backend on Railway
- Frontend on Streamlit Cloud
- Fully managed infrastructure

### **Option 3: Docker** (Full Control)
- Containerized deployment
- Works anywhere Docker runs
- Includes docker-compose.yml

### **Option 4: Heroku**
- One-command deployment
- Legacy but still useful
- Easy scaling

### **Option 5: Google Cloud Run**
- Serverless option
- Pay-per-use pricing
- Auto-scaling built-in

👉 **See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions**

---

## 🔧 Configuration

### **Environment Variables** (.env)
```env
DATABASE_URL=sqlite:///./fashion_supply.db
API_BASE_URL=http://127.0.0.1:8000/api/v1
ENV=development
```

### **Production Setup**
```env
DATABASE_URL=postgresql://user:pass@host/db
API_BASE_URL=https://your-domain.com/api
ENV=production
```

👉 **See [CONFIGURATION.md](CONFIGURATION.md) for all options**

---

## 📈 Usage Examples

### **Check Portfolio Risk**
```bash
curl http://127.0.0.1:8000/api/v1/analytics/risk-summary
```
```json
{
  "risk_distribution": {
    "Low Risk": 12,
    "Medium Risk": 6,
    "High Risk": 2
  },
  "high_risk_products": [...]
}
```

### **Get Restock Recommendations**
```bash
curl http://127.0.0.1:8000/api/v1/recommend/restock
```
```json
{
  "recommendations": [
    {
      "sku": "SKU-0001",
      "current_stock": 5,
      "suggested_quantity": 95,
      "priority": "HIGH"
    }
  ]
}
```

### **Demand Forecast**
```bash
curl http://127.0.0.1:8000/api/v1/predict/demand/1
```
```json
{
  "product_id": 1,
  "forecast_date": "2026-03-25",
  "predicted_demand": 42
}
```

---

## 🏆 Key Features

✅ **Real-time Analytics**
✅ **Multi-product Comparison**
✅ **AI-powered Recommendations**
✅ **Risk-based Alerts**
✅ **Professional Dashboard**
✅ **REST API**
✅ **Production-ready**
✅ **Cloud Deployable**
✅ **Comprehensive Docs**
✅ **Sample Data Included**

---

## 🐛 Troubleshooting

### **Issue: "Connection disconnected"**
```bash
# Make sure API is running:
uvicorn api.main:app --reload
```

### **Issue: "No module named X"**
```bash
# Install dependencies:
pip install -r requirements.txt
```

### **Issue: "Database not found"**
```bash
# Initialize database:
python db/init_db.py
python data/generate_synthetic.py
```

👉 **See [QUICKSTART.md](QUICKSTART.md) for more solutions**

---

## 📚 Learning Path

1. **Start Here**: [QUICKSTART.md](QUICKSTART.md) - 5 minute setup
2. **Explore**: Open dashboard at http://localhost:8501
3. **Learn**: [DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md) - Feature explanations
4. **Build Insights**: [BEST_PRACTICES.md](BEST_PRACTICES.md) - Analysis strategies
5. **Deploy**: [DEPLOYMENT.md](DEPLOYMENT.md) - Share with others

---

## 🔐 Security

### **Production Checklist**
- [ ] Use PostgreSQL for production
- [ ] Enable API authentication
- [ ] Configure CORS properly
- [ ] Use HTTPS only
- [ ] Hide sensitive data in .env
- [ ] Regular backups
- [ ] Audit logs enabled

👉 **See [CONFIGURATION.md](CONFIGURATION.md) for security setup**

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Model accuracy improvements
- Additional visualizations
- Performance optimizations
- More ML features
- Documentation enhancements

---

## 📞 Support

- **Documentation**: See the markdown files in root directory
- **API Docs**: http://127.0.0.1:8000/docs (when running)
- **Issues**: Check QUICKSTART.md troubleshooting section

---

## 📋 Version History

**v2.0** (Current)
- ✨ Complete dashboard redesign with 4-tab interface
- ✨ Enhanced API with 15+ endpoints
- ✨ Advanced analytics and recommendations
- ✨ Professional documentation suite
- ✨ Production-ready deployment options

**v1.0** (Initial)
- Basic single-view dashboard
- Core API endpoints
- Sample ML models

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 🎉 Quick Links

| Resource | URL |
|----------|-----|
| Dashboard | http://localhost:8501 |
| API | http://127.0.0.1:8000 |
| API Docs | http://127.0.0.1:8000/docs |
| Quick Start | [QUICKSTART.md](QUICKSTART.md) |
| Dashboard Guide | [DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md) |
| Deployment | [DEPLOYMENT.md](DEPLOYMENT.md) |
| Configuration | [CONFIGURATION.md](CONFIGURATION.md) |
| Best Practices | [BEST_PRACTICES.md](BEST_PRACTICES.md) |

---

**Ready to get started? Follow [QUICKSTART.md](QUICKSTART.md) to launch in 5 minutes! 🚀**
```

**Terminal 2 (Frontend Interface visualizations mapping locally):**
```powershell
.\venv\Scripts\activate
streamlit run dashboard/app.py
```
