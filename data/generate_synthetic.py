import sys
import os
import random
import numpy as np
from datetime import datetime, timedelta

# Ensure the app root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import SessionLocal
from db.models import Product, Sale, Inventory, SocialPost

def generate_synthetic_data(num_products=20, days=180):
    db = SessionLocal()
    print(f"Generating synthetic dataset for {num_products} products over {days} days...")
    
    try:
        # Clear existing data first
        print("Clearing existing data...")
        db.query(Sale).delete()
        db.query(Inventory).delete()
        db.query(Product).delete()
        db.commit()
        
        # 1. Generate Fashion Products
        categories = ["Tops", "Bottoms", "Outerwear", "Footwear", "Accessories"]
        products = []
        for i in range(1, num_products + 1):
            product = Product(
                sku=f"SKU-{i:04d}",
                name=f"Fashion Model {chr(64 + (i%26))}{i}", # e.g. Fashion Model A1
                category=random.choice(categories),
                base_price=round(random.uniform(19.99, 149.99), 2)
            )
            db.add(product)
            products.append(product)
        db.commit()
        
        # Reload products from DB to ensure IDs are assigned
        products = db.query(Product).all()
        
        # 2. Generate Time Series Data (Sales & Inventory coupling)
        start_date = datetime.now() - timedelta(days=days)
        
        for product in products:
            # We use a mathematical model to simulate realistic demand curves
            # Linear trend
            trend = np.linspace(1, 1.2, days)
            # Sine wave for seasonality peaks
            seasonality = np.sin(np.linspace(0, 3 * np.pi, days)) * 5 + 10
            # Gaussian noise for randomness
            noise = np.random.normal(0, 2, days)
            
            # Combine to form final daily demand
            demand_curve = np.maximum(0, trend * seasonality + noise).astype(int)
            
            # Initial stock buffer
            stock = random.randint(50, 200)
            
            for day in range(days):
                current_date = start_date + timedelta(days=day)
                daily_demand = demand_curve[day]
                
                # Cannot sell more than what is in stock
                sold = min(daily_demand, stock)
                
                if sold > 0:
                    sale = Sale(
                        product_id=product.id,
                        date=current_date,
                        quantity=sold,
                        total_amount=round(sold * product.base_price, 2)
                    )
                    db.add(sale)
                
                # Subtract inventory and trigger restocks mathematically
                stock -= sold
                if stock < 20: 
                    stock += random.randint(50, 150) # Restock bulk
                
                inv = Inventory(
                    product_id=product.id,
                    date=current_date,
                    stock_level=stock,
                    reorder_point=20,
                    lead_time_days=random.randint(3, 10)
                )
                db.add(inv)
                
        # 3. Generate NLP Social Posts for brand perception modeling
        platforms = ["Twitter", "Instagram", "TikTok"]
        sentiments = ["positive", "neutral", "negative"]
        sentiment_bases = {"positive": 0.8, "neutral": 0.5, "negative": 0.2}
        
        for _ in range(num_products * 12): # approx 12 posts per product spanning time
            post_date = start_date + timedelta(days=random.randint(0, days-1))
            sentiment_label = random.choice(sentiments)
            
            post = SocialPost(
                platform=random.choice(platforms),
                content=f"Totally feeling our fashion trends today! {random.choice(['Love it!', 'Okayish', 'Disappointed.'])} #{random.choice(categories).lower()}",
                post_date=post_date,
                likes=random.randint(0, 1500),
                shares=random.randint(0, 200),
                sentiment_score=sentiment_bases[sentiment_label] + random.uniform(-0.1, 0.1)
            )
            db.add(post)
            
        db.commit()
        print(f"Successfully generated database records!")
        print(f"-> {num_products} products generated.")
        print(f"-> {num_products * days} days of sales and inventory timelines simulated.")
        print(f"-> Mock social media posts initialized.")
        
    except Exception as e:
        print(f"Data generation failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Generate 20 products across 180 days (6 months) as prototype baseline
    generate_synthetic_data(num_products=20, days=180) 
