from pydantic import BaseModel
from typing import Optional, List

class ProductBase(BaseModel):
    name: str
    category: str
    base_price: float

class ProductResponse(ProductBase):
    id: int
    sku: str
    class Config:
        from_attributes = True

class RiskPrediction(BaseModel):
    product_id: int
    current_stock: int
    risk_level: str
    action_recommended: str

class DemandForecast(BaseModel):
    product_id: int
    forecast_date: str
    predicted_demand: int

class SentimentAnalysis(BaseModel):
    product_category: str
    average_score: float
    sentiment_label: str
