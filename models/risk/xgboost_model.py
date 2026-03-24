import sys
import os
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from db.database import engine

def fetch_risk_data():
    print("Extracting complex inventory vectors from PostgreSQL schemas...")
    # Join inventory, sales, and products to create a unified structural heuristic footprint
    query = """
    SELECT 
        i.stock_level, 
        i.reorder_point, 
        i.lead_time_days,
        p.base_price,
        COALESCE(s.quantity, 0) as recent_sales
    FROM inventory i
    JOIN products p ON i.product_id = p.id
    LEFT JOIN sales s ON i.product_id = s.product_id AND i.date = s.date
    """
    df = pd.read_sql(query, engine)
    
    if len(df) == 0:
        raise ValueError("No SQL inventory mappings array found. Make sure PostgreSQL populated correctly.")
        
    return df

def generate_risk_labels(df):
    # Synthetically compute risk mappings heuristically dynamically 
    # Risk 2 (High): Sequential stock dropping below reorder triggers natively
    # Risk 1 (Medium): Supply decay stable but dipping close
    # Risk 0 (Low): Supply completely stable
    
    conditions = [
        (df['stock_level'] <= df['reorder_point'] * 1.5) & (df['recent_sales'] > 0), # High constraints
        (df['stock_level'] <= df['reorder_point'] * 3.0), # Medium constraints
    ]
    choices = [2, 1]
    df['risk_class'] = np.select(conditions, choices, default=0) # 0 maps Low baseline
    return df

def train_xgboost():
    print("Initializing XGBoost Inventory Optimization Core Algorithm...")
    
    # 1. Pipeline mapping
    df = fetch_risk_data()
    df = generate_risk_labels(df)
    
    X = df[['stock_level', 'reorder_point', 'lead_time_days', 'base_price', 'recent_sales']]
    y = df['risk_class']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 2. Structural gradient boosting mapping parameters natively
    model = xgb.XGBClassifier(
        objective='multi:softmax',
        num_class=3,
        max_depth=5,
        learning_rate=0.1,
        n_estimators=100,
        eval_metric='mlogloss',
        use_label_encoder=False
    )
    
    print(f"Executing XGBoost parallelized mathematical descent trees on {len(X_train)} mapped sequences...")
    model.fit(X_train, y_train)
    
    # 3. Model boundary evaluations natively mapped
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Optimal Multiclass classification structure Accuracy metric: {acc:.4f}")
    
    print("\nCategorized Boundaries Matrix:")
    print(classification_report(y_test, y_pred, target_names=['Low Risk', 'Medium Risk', 'High Risk']))
    
    # 4. Checkpoint creation
    out_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)
    save_path = os.path.join(out_dir, "xgb_risk_v1.pkl")
    
    joblib.dump(model, save_path)
    print(f"Extreme Gradient Optimized binary weights reliably saved -> {save_path}")

if __name__ == "__main__":
    train_xgboost()
