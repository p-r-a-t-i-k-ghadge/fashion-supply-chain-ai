# ⚙️ Configuration Guide

Complete configuration instructions for your Fashion Supply Chain AI Dashboard.

---

## **📁 Environment Variables Setup**

### **1. Local Development (.env file)**

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=sqlite:///./fashion_supply.db
# For PostgreSQL: postgresql://user:password@localhost:5432/fashion_db

# API Configuration
API_HOST=127.0.0.1
API_PORT=8000
API_DEBUG=True

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=False

# Application Settings
ENV=development
LOG_LEVEL=INFO
```

### **2. Production Deployment (.env.production)**

```env
# Database (Use PostgreSQL for production)
DATABASE_URL=postgresql://user:password@db-host:5432/fashion_supply

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=False

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=True

# Application Settings
ENV=production
LOG_LEVEL=WARNING

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=["https://your-domain.com"]
```

---

## **🗄️ Database Configuration**

### **Using SQLite (Default)**
```python
# db/database.py already configured
DATABASE_URL = "sqlite:///./fashion_supply.db"
```
✅ **Pros**: No setup required, great for testing
❌ **Cons**: Not suitable for production, limited concurrency

### **Switching to PostgreSQL**

1. **Install PostgreSQL**:
   ```bash
   # Windows: Download from https://www.postgresql.org/download/windows/
   # Mac: brew install postgresql
   # Linux: sudo apt-get install postgresql
   ```

2. **Create database**:
   ```sql
   CREATE DATABASE fashion_supply;
   CREATE USER fashion_user WITH PASSWORD 'your_password';
   ALTER ROLE fashion_user SET client_encoding TO 'utf8';
   ALTER ROLE fashion_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE fashion_user SET default_transaction_deferrable TO on;
   GRANT ALL PRIVILEGES ON DATABASE fashion_supply TO fashion_user;
   ```

3. **Update .env**:
   ```env
   DATABASE_URL=postgresql://fashion_user:your_password@localhost:5432/fashion_supply
   ```

4. **Install PostgreSQL driver**:
   ```bash
   pip install psycopg2-binary
   ```

5. **Update requirements.txt**:
   ```
   psycopg2-binary==2.9.9
   ```

---

## **🔐 Security Configuration**

### **API Security**

1. **Enable CORS (if needed)**

Create a file `api/cors_config.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8501",
    "https://your-domain.com"
]

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
```

In `api/main.py`:
```python
from api.cors_config import setup_cors
app = setup_cors(app)
```

2. **Add API Key Authentication**

Create `api/security.py`:
```python
from fastapi import Depends, HTTPException, Header
from typing import Optional

async def verify_api_key(x_token: Optional[str] = Header(None)):
    if x_token != "your-secret-api-key":
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_token

# Then add to endpoints:
@router.get("/products")
def get_products(api_key: str = Depends(verify_api_key)):
    # ...
```

3. **Enable HTTPS**

```python
# In api/main.py
import ssl

# For production
ssl_keyfile = "path/to/key.pem"
ssl_certfile = "path/to/cert.pem"

# Then run:
# uvicorn api.main:app --ssl-keyfile=$ssl_keyfile --ssl-certfile=$ssl_certfile
```

---

## **📊 Streamlit Configuration**

### **Local Development** (`.streamlit/config.toml`)

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true
toolbarMode = "developer"

[server]
headless = false
runOnSave = true
logger.level = "info"

[browser]
gatherUsageStats = false
```

### **Production** (.streamlit/secrets.toml)

```toml
# API Configuration
API_BASE_URL = "https://api.your-domain.com"

# Database (for direct access if needed)
DATABASE_URL = "postgresql://user:pass@host/db"

# Credentials
SECRET_KEY = "your-secret-key"
```

---

## **🔧 Application Settings**

### **Dashboard Configuration** (dashboard/config.py)

Create this file:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Settings
    API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api/v1")
    API_TIMEOUT = 30
    
    # Database Settings
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fashion_supply.db")
    
    # Streamlit Settings
    PAGE_TITLE = "Fashion Supply Chain AI"
    PAGE_ICON = "📦"
    LAYOUT = "wide"
    
    # Cache Settings
    CACHE_TTL = 60  # seconds
    
    # Data Settings
    MAX_PRODUCTS = 100
    MAX_DATE_RANGE = 180  # days
    
    # Feature Flags
    ENABLE_SENTIMENT = True
    ENABLE_FORECASTING = True
    ENABLE_RISK_SCORING = True
    
    # Environment
    ENV = os.getenv("ENV", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings()
```

Then use in dashboard:
```python
from dashboard.config import settings

API_BASE_URL = settings.API_BASE_URL
st.set_page_config(
    page_title=settings.PAGE_TITLE,
    page_icon=settings.PAGE_ICON,
    layout=settings.LAYOUT
)
```

---

## **🚀 Deployment Configuration**

### **For Streamlit Cloud**

Create `.streamlit/secrets.toml`:
```toml
API_BASE_URL = "https://your-api.railway.app/api/v1"
DATABASE_URL = "postgresql://user:pass@your-db-host/fashion_supply"
```

### **For Docker**

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: fashion_user
      POSTGRES_PASSWORD: your_password
      POSTGRES_DB: fashion_supply
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://fashion_user:your_password@postgres:5432/fashion_supply
      ENV: production
    depends_on:
      - postgres
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000

  dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      API_BASE_URL: http://api:8000/api/v1
    depends_on:
      - api
    command: streamlit run dashboard/app.py

volumes:
  postgres_data:
```

### **For Heroku**

Create `.env.heroku`:
```env
DATABASE_URL=postgresql://user:pass@heroku-postgres-host/fashion_db
ENV=production
PYTHON_VERSION=3.13.5
```

Deploy:
```bash
heroku config:set DATABASE_URL="your-db-url"
git push heroku main
```

---

## **📝 Logging Configuration**

Create `logging_config.py`:
```python
import logging
import logging.handlers
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

def setup_logging():
    logger = logging.getLogger("fashion_supply")
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        "logs/app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Usage in code
logger = setup_logging()
logger.info("Application started")
```

---

## **🎯 Feature Flags**

Create `config/features.py`:
```python
import os

FEATURES = {
    "SENTIMENT_ANALYSIS": os.getenv("FEATURE_SENTIMENT", "true").lower() == "true",
    "LSTM_FORECASTING": os.getenv("FEATURE_LSTM", "true").lower() == "true",
    "XGBOOST_RISK": os.getenv("FEATURE_XGBOOST", "true").lower() == "true",
    "MULTI_PRODUCT_COMPARE": os.getenv("FEATURE_COMPARE", "true").lower() == "true",
    "EXPORT_CSV": os.getenv("FEATURE_EXPORT", "true").lower() == "true",
}

def is_feature_enabled(feature_name):
    return FEATURES.get(feature_name, False)
```

Usage:
```python
from config.features import is_feature_enabled

if is_feature_enabled("SENTIMENT_ANALYSIS"):
    # Show sentiment tab
    pass
```

---

## **🔄 Update Procedures**

### **Updating Dependencies**

```bash
# Check for outdated packages
pip list --outdated

# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade fastapi

# Save new versions
pip freeze > requirements.txt
```

### **Database Migrations**

```bash
# Add new column
python db/migrations.py add_column table_name column_name String

# Create backup before migration
python db/backup.py

# Apply migration
python db/init_db.py
```

---

## **✅ Configuration Checklist**

- [ ] `.env` file created with database URL
- [ ] `.streamlit/config.toml` configured
- [ ] Database initialized: `python db/init_db.py`
- [ ] Sample data generated: `python data/generate_synthetic.py`
- [ ] API running: `uvicorn api.main:app --reload`
- [ ] Dashboard running: `streamlit run dashboard/app.py`
- [ ] Both services accessible and connected
- [ ] CORS configured for deployment
- [ ] Logging setup complete
- [ ] Security settings reviewed

---

## **🆘 Quick Troubleshooting**

| Issue | Solution |
|-------|----------|
| Database connection fails | Check DATABASE_URL in .env |
| API not found | Ensure API_BASE_URL is correct |
| Slow performance | Check database indexes, enable caching |
| CORS errors | Verify CORS origins configuration |
| Missing modules | Run `pip install -r requirements.txt` |

---

**Configuration complete! 🎉**

Ready to deploy? See **DEPLOYMENT.md**