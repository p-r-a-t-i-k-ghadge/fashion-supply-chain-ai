from fastapi import FastAPI
from api.routes import products
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title=os.getenv("PROJECT_NAME", "AI Supply Chain Dynamics Core API"),
    version=os.getenv("MODEL_VERSION", "v1.0.0"),
    description="Multi-modal decoupled Backend Architecture serving PyTorch / XGBoost structures instantly."
)

app.include_router(products.router, prefix="/api/v1", tags=["AI Predictions Endpoint Arrays"])

@app.get("/")
def health_check():
    return {"status": "Operational", "framework": "FastAPI Vector Backend Initialized Matrix!"}
