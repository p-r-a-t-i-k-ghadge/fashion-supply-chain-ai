import sys
import os

# Ensure the parent directory is in the path to allow importing db module properly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import engine, Base
# Import all models so metadata gets registered
from db.models import Product, Sale, Inventory, SocialPost, BrandMetric, ForecastResult, RiskScore

def create_tables():
    print("Creating database tables in PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!!")

if __name__ == "__main__":
    create_tables()
