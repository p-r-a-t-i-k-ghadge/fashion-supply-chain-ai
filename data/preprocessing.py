import sys
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import engine

def load_data_from_db():
    print("Extracting raw data from PostgreSQL via SQLAlchemy...")
    sales_df = pd.read_sql("SELECT * FROM sales", engine)
    inventory_df = pd.read_sql("SELECT * FROM inventory", engine)
    products_df = pd.read_sql("SELECT id as product_id, sku, category, base_price FROM products", engine)
    posts_df = pd.read_sql("SELECT * FROM social_posts", engine)
    return sales_df, inventory_df, products_df, posts_df

def preprocess_time_series(sales_df, inventory_df, products_df):
    print("Preprocessing time-series data for LSTM Demand Forecasting...")
    
    # Normalize datetimes to date-only
    sales_df['date'] = pd.to_datetime(sales_df['date']).dt.normalize()
    inventory_df['date'] = pd.to_datetime(inventory_df['date']).dt.normalize()
    
    # Group by product and date to flatten multi-sale days
    daily_sales = sales_df.groupby(['product_id', 'date'])['quantity'].sum().reset_index()
    daily_inv = inventory_df.groupby(['product_id', 'date'])['stock_level'].last().reset_index()
    
    # Outer join to capture days with inventory but 0 sales
    merged_df = pd.merge(daily_sales, daily_inv, on=['product_id', 'date'], how='outer').fillna({'quantity': 0})
    merged_df['stock_level'] = merged_df.groupby('product_id')['stock_level'].ffill().fillna(0) # Forward fill missing stock
    
    # Join product metadata
    merged_df = pd.merge(merged_df, products_df, on='product_id', how='left')
    
    # Feature Engineering (Temporal)
    merged_df['day_of_week'] = merged_df['date'].dt.dayofweek
    merged_df['month'] = merged_df['date'].dt.month
    
    # Sort for time-series sequence preservation
    merged_df = merged_df.sort_values(by=['product_id', 'date']).reset_index(drop=True)
    
    # Feature Scaling (Deep Learning strictly bounds inputs [0, 1])
    scaler = MinMaxScaler()
    continuous_features = ['quantity', 'stock_level', 'base_price']
    merged_df[continuous_features] = scaler.fit_transform(merged_df[continuous_features])
    
    print(f"-> Processed {len(merged_df)} daily record mappings across all SKUs.")
    return merged_df, scaler

def preprocess_nlp(posts_df):
    print("Preprocessing text data for BERT Sentiment Analysis...")
    # Clean NaNs and normalize text
    posts_df = posts_df.dropna(subset=['content'])
    posts_df['cleaned_content'] = posts_df['content'].astype(str).str.lower().str.replace(r'\s+', ' ', regex=True)
    
    # Split text corpus 80/20 train/validation
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        posts_df['cleaned_content'].tolist(), 
        posts_df['sentiment_score'].tolist(), 
        test_size=0.2, 
        random_state=42
    )
    
    print(f"-> Prepared {len(train_texts)} training texts and {len(val_texts)} validation texts.")
    return train_texts, val_texts, train_labels, val_labels

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "processed")
    os.makedirs(out_dir, exist_ok=True)
    
    sales, inventory, products, posts = load_data_from_db()
    
    # 1. Export standardized time series matrices
    ts_data, ts_scaler = preprocess_time_series(sales, inventory, products)
    ts_data.to_csv(os.path.join(out_dir, "time_series_ready.csv"), index=False)
    
    # 2. Extract NLP corpuses
    tr_txt, val_txt, tr_lbl, val_lbl = preprocess_nlp(posts)
    
    print("Data Preprocessing pipeline successfully completed!")
    print(f"Cleaned tensors safely exported to {out_dir}/time_series_ready.csv")
