from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, index=True)
    base_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    sales = relationship("Sale", back_populates="product")
    inventory = relationship("Inventory", back_populates="product")
    forecasts = relationship("ForecastResult", back_populates="product")
    risks = relationship("RiskScore", back_populates="product")

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    date = Column(DateTime, index=True)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Float)

    product = relationship("Product", back_populates="sales")

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    date = Column(DateTime, index=True)
    stock_level = Column(Integer, nullable=False)
    reorder_point = Column(Integer)
    lead_time_days = Column(Integer)

    product = relationship("Product", back_populates="inventory")

class SocialPost(Base):
    __tablename__ = 'social_posts'
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)
    content = Column(Text, nullable=False)
    post_date = Column(DateTime, index=True)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    sentiment_score = Column(Float, nullable=True) 

class BrandMetric(Base):
    __tablename__ = 'brand_metrics'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    overall_sentiment_score = Column(Float)
    trending_keywords = Column(Text)

class ForecastResult(Base):
    __tablename__ = 'forecast_results'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    forecast_date = Column(DateTime, index=True)
    predicted_demand = Column(Float, nullable=False)
    confidence_interval_lower = Column(Float)
    confidence_interval_upper = Column(Float)
    model_version = Column(String)

    product = relationship("Product", back_populates="forecasts")

class RiskScore(Base):
    __tablename__ = 'risk_scores'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    date = Column(DateTime, index=True)
    risk_level = Column(String, index=True)
    risk_probability = Column(Float)
    contributing_factors = Column(Text)

    product = relationship("Product", back_populates="risks")
