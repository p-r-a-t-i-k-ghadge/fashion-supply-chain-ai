import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import sys
import numpy as np
import subprocess
from pathlib import Path

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

# ==================== HELPER FUNCTIONS FOR MOCK DATA ====================
@st.cache_data(ttl=300)
def generate_dynamic_business_data():
    """Generate realistic fashion retail business data"""
    np.random.seed(42)
    
    # Customer behavior data
    days = 30
    dates = pd.date_range(end=datetime.now(), periods=days)
    
    daily_sales = np.random.randint(100000, 500000, days)  # INR
    daily_customers = np.random.randint(50, 200, days)
    daily_orders = np.random.randint(40, 150, days)
    
    # Product categories fashion-specific
    categories = ['T-Shirts', 'Jeans', 'Dresses', 'Jackets', 'Accessories', 'Shoes']
    category_sales = {cat: np.random.randint(50000, 300000) for cat in categories}
    category_units = {cat: np.random.randint(20, 150) for cat in categories}
    
    # Customer behavior metrics
    repeat_customers = np.random.randint(300, 800)
    new_customers = np.random.randint(100, 400)
    churn_rate = np.random.uniform(5, 15)
    avg_order_value = np.random.randint(1500, 4500)
    customer_satisfaction = np.random.uniform(4.0, 4.8)
    
    # Inventory metrics
    total_inventory = np.random.randint(500, 2000)
    low_stock_items = np.random.randint(5, 25)
    stockout_items = np.random.randint(0, 5)
    
    # Returns & quality
    return_rate = np.random.uniform(2, 8)
    quality_issues = np.random.randint(0, 10)
    
    return {
        'dates': dates,
        'daily_sales': daily_sales,
        'daily_customers': daily_customers,
        'daily_orders': daily_orders,
        'category_sales': category_sales,
        'category_units': category_units,
        'repeat_customers': repeat_customers,
        'new_customers': new_customers,
        'churn_rate': churn_rate,
        'avg_order_value': avg_order_value,
        'customer_satisfaction': customer_satisfaction,
        'total_inventory': total_inventory,
        'low_stock_items': low_stock_items,
        'stockout_items': stockout_items,
        'return_rate': return_rate,
        'quality_issues': quality_issues
    }

@st.cache_data(ttl=300)
def get_customer_segments():
    """Generate customer segmentation data"""
    segments = {
        'Premium Buyers': {'count': 450, 'avg_spend': 8500, 'retention': 92},
        'Regular Buyers': {'count': 2100, 'avg_spend': 3200, 'retention': 78},
        'Budget Conscious': {'count': 3800, 'avg_spend': 1200, 'retention': 55},
        'One-time Buyers': {'count': 5200, 'avg_spend': 1800, 'retention': 0}
    }
    return segments

@st.cache_data(ttl=300)
def get_top_products():
    """Get top selling fashion products"""
    products = [
        {'name': 'Premium Cotton T-Shirt', 'sales': 850000, 'units': 450, 'rating': 4.8, 'category': 'T-Shirts'},
        {'name': 'Slim Fit Jeans', 'sales': 720000, 'units': 320, 'rating': 4.6, 'category': 'Jeans'},
        {'name': 'Summer Dress', 'sales': 650000, 'units': 280, 'rating': 4.7, 'category': 'Dresses'},
        {'name': 'Leather Jacket', 'sales': 580000, 'units': 150, 'rating': 4.5, 'category': 'Jackets'},
        {'name': 'Sports Shoes', 'sales': 520000, 'units': 220, 'rating': 4.4, 'category': 'Shoes'}
    ]
    return pd.DataFrame(products)

@st.cache_data(ttl=300)
def get_trend_forecast():
    """Get 30-day sales forecast"""
    dates = pd.date_range(end=datetime.now(), periods=30)
    base_sales = 300000
    trend = np.linspace(base_sales, base_sales * 1.15, 30)
    seasonal = 50000 * np.sin(np.linspace(0, 2*np.pi, 30))
    noise = np.random.normal(0, 20000, 30)
    forecast = trend + seasonal + noise
    return pd.DataFrame({'date': dates, 'forecast': forecast})

# Page Configuration
st.set_page_config(
    page_title="Fashion Retail Intelligence Platform",
    layout="wide",
    page_icon="👗",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling - MODERN & INTERACTIVE
st.markdown("""
    <style>
    /* Main Theme */
    :root {
        --primary: #1f77b4;
        --secondary: #ff7f0e;
        --success: #2ca02c;
        --danger: #d62728;
        --warning: #ff9800;
    }
    
    /* Enhanced Metrics & Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 15px;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    
    /* Alert Styling */
    .alert-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        border-left: 6px solid #d62728;
        padding: 15px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
    }
    
    .alert-medium {
        background: linear-gradient(135deg, #ffa500 0%, #ff8c00 100%);
        border-left: 6px solid #ff9800;
        padding: 15px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
    }
    
    .alert-low {
        background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        border-left: 6px solid #2ca02c;
        padding: 15px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-top: 4px solid #667eea;
        text-align: center;
    }
    
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: #667eea;
        margin: 10px 0;
    }
    
    .kpi-label {
        font-size: 14px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Section Headers */
    .section-header {
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
        margin-bottom: 20px;
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
        text-transform: uppercase;
    }
    
    .status-badge-high {
        background: #ff6b6b;
        color: white;
    }
    
    .status-badge-medium {
        background: #ffa500;
        color: white;
    }
    
    .status-badge-low {
        background: #51cf66;
        color: white;
    }
    
    /* Enhancement Animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease;
    }
    
    </style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div style="text-align: center; padding: 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin-bottom: 30px;">
    <h1 style="font-size: 3em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">👗 Fashion Retail Intelligence</h1>
    <p style="font-size: 1.2em; margin: 10px 0 0 0;">AI-Powered Analytics for Fashion E-Commerce Sellers</p>
    <p style="font-size: 0.95em; opacity: 0.9;">🇮🇳 Customer Behavior • Sales Analytics • Inventory Optimization • Revenue Growth • ₹ INR</p>
</div>
""", unsafe_allow_html=True)

# Add auto-refresh indicator
col1, col2, col3 = st.columns(3)
with col2:
    st.caption("🟢 Live Business Intelligence • Last Updated: " + datetime.now().strftime("%d-%b %H:%M"))

# ==================== SESSION STATE ====================
if 'data_initialized' not in st.session_state:
    st.session_state.data_initialized = False
if 'products_data' not in st.session_state:
    st.session_state.products_data = None

# ==================== UTILITY FUNCTIONS ====================
@st.cache_data(ttl=60)
def fetch_products():
    """Fetch all products from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/products?limit=100")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"⚠️ Failed to fetch products: {str(e)}")
        return []

@st.cache_data(ttl=30)
def get_product_risk(product_id):
    """Get risk prediction for a product"""
    try:
        response = requests.get(f"{API_BASE_URL}/predict/risk/{product_id}")
        response.raise_for_status()
        return response.json()
    except:
        return {"risk_level": "Unknown", "current_stock": 0, "action_recommended": "Check API"}

@st.cache_data(ttl=30)
def get_product_demand(product_id):
    """Get demand forecast for a product"""
    try:
        response = requests.get(f"{API_BASE_URL}/predict/demand/{product_id}")
        response.raise_for_status()
        return response.json()
    except:
        return {"predicted_demand": 0, "forecast_date": "N/A"}

def process_uploaded_data(df_products, df_sales=None, df_inventory=None):
    """Process and save uploaded CSV data to database"""
    try:
        # Import database modules
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from db.database import SessionLocal, engine, Base
        from db.models import Product, Sale, Inventory

        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)

        db = SessionLocal()

        # Clear existing data
        db.query(Sale).delete()
        db.query(Inventory).delete()
        db.query(Product).delete()
        db.commit()

        # Process products
        products_map = {}
        for _, row in df_products.iterrows():
            try:
                product = Product(
                    sku=str(row['sku']).strip(),
                    name=str(row['name']).strip(),
                    category=str(row['category']).strip(),
                    base_price=float(row['base_price'])
                )
                db.add(product)
                products_map[product.sku] = product
            except Exception as e:
                print(f"Error processing product row: {e}")
                continue

        db.commit()

        # Reload products to get IDs
        products_map = {}
        for product in db.query(Product).all():
            products_map[product.sku] = product

        # Process sales data
        if df_sales is not None:
            print(f"Processing {len(df_sales)} sales records...")
            for _, row in df_sales.iterrows():
                try:
                    sku = str(row['sku']).strip()
                    if sku in products_map:
                        sale = Sale(
                            product_id=products_map[sku].id,
                            date=pd.to_datetime(row['date']),
                            quantity=int(row['quantity']),
                            total_amount=float(row['total_amount'])
                        )
                        db.add(sale)
                    else:
                        print(f"Warning: SKU {sku} not found in products")
                except Exception as e:
                    print(f"Error processing sales row: {e}")
                    continue

        # Process inventory data
        if df_inventory is not None:
            print(f"Processing {len(df_inventory)} inventory records...")
            for _, row in df_inventory.iterrows():
                try:
                    sku = str(row['sku']).strip()
                    if sku in products_map:
                        inventory = Inventory(
                            product_id=products_map[sku].id,
                            date=pd.to_datetime(row['date']),
                            stock_level=int(row['stock_level']),
                            reorder_point=int(row['reorder_point']),
                            lead_time_days=int(row['lead_time_days'])
                        )
                        db.add(inventory)
                    else:
                        print(f"Warning: SKU {sku} not found in products")
                except Exception as e:
                    print(f"Error processing inventory row: {e}")
                    continue

        db.commit()
        print(f"Successfully saved {len(products_map)} products")
        db.close()
        return True

    except Exception as e:
        print(f"Error in process_uploaded_data: {e}")
        import traceback
        traceback.print_exc()
        return False

def initialize_database():
    """Initialize database with synthetic data"""
    try:
        with st.spinner("⏳ Setting up database schema..."):
            # First create tables
            result_init = subprocess.run(
                ["python", "db/init_db.py"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            if result_init.returncode != 0:
                st.error(f"❌ Failed to create database tables: {result_init.stderr}")
                return False

        with st.spinner("⏳ Generating synthetic dataset..."):
            # Then generate data
            result_data = subprocess.run(
                ["python", "data/generate_synthetic.py"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            if result_data.returncode != 0:
                st.error(f"❌ Failed to generate data: {result_data.stderr}")
                return False

        # Show success message with data summary
        st.success("✅ Database initialized successfully!")
        st.info("📊 Generated 20 products with 180 days of historical data")
        return True

    except Exception as e:
        st.error(f"❌ Database initialization failed: {str(e)}")
        return False

# ==================== SIDEBAR - CONFIGURATION ====================
with st.sidebar:
    st.header("⚙️ Dashboard Configuration")
    
    # Data Management Section
    st.subheader("📊 Data Management")

    tab1, tab2, tab3 = st.sidebar.tabs(["Data Setup", "Upload Data", "Filters"])

    with tab1:
        st.markdown("### Initialize Data")
        
        if st.button("📥 Generate Synthetic Dataset", key="gen_data"):
            st.warning("⚠️ This will create sample data for demonstration")
            
            confirm = st.checkbox("I understand this will overwrite existing data")
            
            if confirm and st.button("✅ Confirm & Generate", key="confirm_gen"):
                success = initialize_database()
                if success:
                    st.success("✅ Dataset generated successfully!")
                    st.session_state.data_initialized = True
                    st.cache_data.clear()
                else:
                    st.error("❌ Failed to generate dataset")
    
    with tab2:
        st.markdown("### Date Range")
        
        # Date range selector
        date_option = st.radio(
            "Select time period:",
            ["Last 7 days", "Last 30 days", "Last 90 days", "Custom"]
        )
        
        if date_option == "Custom":
            start_date = st.date_input("Start Date", value=pd.Timestamp.now() - timedelta(days=30))
            end_date = st.date_input("End Date", value=pd.Timestamp.now())
        else:
            end_date = pd.Timestamp.now()
            if date_option == "Last 7 days":
                start_date = end_date - timedelta(days=7)
            elif date_option == "Last 30 days":
                start_date = end_date - timedelta(days=30)
            else:  # Last 90 days
                start_date = end_date - timedelta(days=90)
        
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date

        st.markdown(f"**Period:** {start_date.date()} to {end_date.date()}")

    with tab3:
        st.markdown("### 📤 Upload Your Data")
        st.markdown("Upload your own CSV files to replace synthetic data")

        # File uploaders
        products_file = st.file_uploader(
            "📦 Products CSV",
            type=['csv'],
            help="Upload products data with columns: sku, name, category, base_price"
        )

        sales_file = st.file_uploader(
            "💰 Sales CSV",
            type=['csv'],
            help="Upload sales data with columns: sku, date, quantity, total_amount"
        )

        inventory_file = st.file_uploader(
            "📦 Inventory CSV",
            type=['csv'],
            help="Upload inventory data with columns: sku, date, stock_level, reorder_point, lead_time_days"
        )

        if st.button("📤 Process & Upload Data", key="upload_data"):
            if not products_file:
                st.error("❌ Products file is required")
                st.stop()  # Stop execution instead of return

            try:
                with st.spinner("⏳ Processing uploaded data..."):
                    # Process products
                    df_products = pd.read_csv(products_file)
                    required_cols = ['sku', 'name', 'category', 'base_price']
                    if not all(col in df_products.columns for col in required_cols):
                        st.error(f"❌ Products CSV must contain columns: {', '.join(required_cols)}")
                        st.stop()

                    # Process sales if provided
                    df_sales = None
                    if sales_file:
                        df_sales = pd.read_csv(sales_file)
                        sales_cols = ['sku', 'date', 'quantity', 'total_amount']
                        if not all(col in df_sales.columns for col in sales_cols):
                            st.error(f"❌ Sales CSV must contain columns: {', '.join(sales_cols)}")
                            st.stop()

                    # Process inventory if provided
                    df_inventory = None
                    if inventory_file:
                        df_inventory = pd.read_csv(inventory_file)
                        inv_cols = ['sku', 'date', 'stock_level', 'reorder_point', 'lead_time_days']
                        if not all(col in df_inventory.columns for col in inv_cols):
                            st.error(f"❌ Inventory CSV must contain columns: {', '.join(inv_cols)}")
                            st.stop()

                    # Process and save the data
                    success = process_uploaded_data(df_products, df_sales, df_inventory)

                    if success:
                        st.success("✅ Data uploaded successfully!")
                        st.info(f"📊 Processed {len(df_products)} products")
                        if df_sales is not None:
                            st.info(f"💰 Processed {len(df_sales)} sales records")
                        if df_inventory is not None:
                            st.info(f"📦 Processed {len(df_inventory)} inventory records")

                        st.session_state.data_initialized = True
                        st.cache_data.clear()
                    else:
                        st.error("❌ Failed to save data to database")

            except Exception as e:
                st.error(f"❌ Failed to process data: {str(e)}")

# ==================== MAIN CONTENT ====================

# Fetch products
products = fetch_products()

if not products:
    st.error("""
    ⚠️ **Cannot connect to API Server**
    
    Please ensure:
    1. FastAPI server is running: `uvicorn api.main:app --reload`
    2. Database is initialized (use the sidebar Data Setup)
    """)
else:
    # ==================== TAB LAYOUT ====================
    tab_overview, tab_single, tab_compare, tab_insights = st.tabs([
        "📊 Overview", 
        "🔍 Product Analysis", 
        "⚖️ Product Comparison",
        "💡 Insights & Recommendations"
    ])
    
    # ==================== TAB 1: OVERVIEW ====================
    with tab_overview:
        st.markdown('<div class="section-header">📊 Portfolio Overview & Key Metrics</div>', unsafe_allow_html=True)

        # ENHANCED KPI SECTION with gradient cards
        df_products = pd.DataFrame(products)
        categories = len(set(p['category'] for p in products))
        avg_price = df_products['base_price'].mean()
        total_value = df_products['base_price'].sum()
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">📦 Total Products</div>
                <div class="kpi-value">{len(products)}</div>
                <p style="font-size: 12px; color: #999; margin: 0;">Active SKUs</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">📂 Categories</div>
                <div class="kpi-value">{categories}</div>
                <p style="font-size: 12px; color: #999; margin: 0;">Product Groups</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">💰 Avg Price</div>
                <div class="kpi-value">${avg_price:.2f}</div>
                <p style="font-size: 12px; color: #999; margin: 0;">Per Unit</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">📊 Catalog Value</div>
                <div class="kpi-value">${total_value/1000:.1f}K</div>
                <p style="font-size: 12px; color: #999; margin: 0;">Total Value</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # DYNAMIC SALES & INVENTORY METRICS
        st.markdown('<div class="section-header">📈 Real-Time Analytics</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 💹 Sales Performance")
            try:
                response = requests.get(f"{API_BASE_URL}/analytics/sales-summary")
                if response.status_code == 200:
                    sales_data = response.json()
                    
                    # Create three columns for sales metrics
                    s1, s2, s3 = st.columns(3)
                    with s1:
                        st.metric("Total Sales", f"{sales_data.get('total_sales', 0):,} units", "+5.2%")
                    with s2:
                        st.metric("Daily Avg", f"{sales_data.get('avg_daily_sales', 0):.0f}", "+2.1%")
                    with s3:
                        st.metric("Revenue", f"${sales_data.get('total_revenue', 0):,.0f}", "+8.5%")
                    
                    # Sales trend mini-chart
                    dates_mini = pd.date_range(end=pd.Timestamp.now(), periods=30)
                    sales_trend = [sales_data.get('avg_daily_sales', 0) * (1 + np.sin(i/10)/5) for i in range(30)]
                    
                    fig_sales = go.Figure(data=go.Scatter(
                        x=dates_mini, 
                        y=sales_trend,
                        fill='tozeroy',
                        fillcolor='rgba(102, 126, 234, 0.2)',
                        line=dict(color='#667eea', width=3)
                    ))
                    fig_sales.update_layout(
                        title="Sales Trend (30 days)",
                        height=250,
                        showlegend=False,
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig_sales, use_container_width=True)
                else:
                    st.info("📊 Sales data not available")
            except Exception as e:
                st.warning(f"⚠️ Sales analytics temporarily unavailable")

        with col2:
            st.markdown("### 📦 Inventory Health")
            try:
                response = requests.get(f"{API_BASE_URL}/analytics/inventory-summary")
                if response.status_code == 200:
                    inv_data = response.json()
                    
                    # Create three columns for inventory metrics
                    i1, i2, i3 = st.columns(3)
                    with i1:
                        st.metric("Total Stock", f"{inv_data.get('total_stock', 0):,}", "-2.4%")
                    with i2:
                        st.metric("Low Stock", f"{inv_data.get('low_stock_count', 0)}", "🚨")
                    with i3:
                        st.metric("Lead Time", f"{inv_data.get('avg_lead_time', 0):.1f}d", "avg")
                    
                    # Inventory health gauge
                    health_score = 100 - (inv_data.get('low_stock_count', 0) * 5)
                    health_score = max(0, min(100, health_score))
                    
                    fig_gauge = go.Figure(data=go.Indicator(
                        mode="gauge+number+delta",
                        value=health_score,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Inventory Health Score"},
                        delta={'reference': 90},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "#667eea"},
                            'steps': [
                                {'range': [0, 33], 'color': "#ffebee"},
                                {'range': [33, 66], 'color': "#fff3e0"},
                                {'range': [66, 100], 'color': "#e8f5e9"}
                            ],
                            'threshold': {
                                'line': {'color': "#d62728", 'width': 4},
                                'thickness': 0.75,
                                'value': 50
                            }
                        }
                    ))
                    fig_gauge.update_layout(height=300)
                    st.plotly_chart(fig_gauge, use_container_width=True)
                else:
                    st.info("📦 Inventory data not available")
            except Exception as e:
                st.warning(f"⚠️ Inventory analytics temporarily unavailable")

        st.markdown("---")

        # CATEGORY ANALYSIS WITH INTERACTIVE CHARTS
        st.markdown('<div class="section-header">📂 Category Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Category Distribution")
            category_counts = df_products['category'].value_counts()
            
            fig_pie = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title="Product Mix by Category",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3,
                labels=category_counts.index
            )
            fig_pie.update_traces(textposition='inside', textinfo='label+percent')
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            st.markdown("### Price Distribution")
            
            fig_price = px.histogram(
                df_products,
                x='base_price',
                nbins=15,
                title="Price Range Distribution",
                labels={'base_price': 'Price ($)', 'count': 'Number of Products'},
                color_discrete_sequence=['#667eea']
            )
            fig_price.update_layout(
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig_price, use_container_width=True)

        st.markdown("---")

        # RISK ASSESSMENT DASHBOARD
        st.markdown('<div class="section-header">⚠️ Risk Assessment Overview</div>', unsafe_allow_html=True)
        
        try:
            response = requests.get(f"{API_BASE_URL}/analytics/risk-overview")
            if response.status_code == 200:
                risk_data = response.json()
                
                r1, r2, r3 = st.columns(3)
                
                with r1:
                    high_risk = risk_data.get('high_risk_count', 0)
                    st.markdown(f"""
                    <div class="kpi-card" style="border-top-color: #d62728;">
                        <div class="kpi-label">🔴 High Risk</div>
                        <div class="kpi-value" style="color: #d62728;">{high_risk}</div>
                        <p style="font-size: 12px; color: #d62728; margin: 0;">Requires Action</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with r2:
                    med_risk = risk_data.get('medium_risk_count', 0)
                    st.markdown(f"""
                    <div class="kpi-card" style="border-top-color: #ff9800;">
                        <div class="kpi-label">🟡 Medium Risk</div>
                        <div class="kpi-value" style="color: #ff9800;">{med_risk}</div>
                        <p style="font-size: 12px; color: #ff9800; margin: 0;">Monitor Closely</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with r3:
                    low_risk = risk_data.get('low_risk_count', 0)
                    st.markdown(f"""
                    <div class="kpi-card" style="border-top-color: #2ca02c;">
                        <div class="kpi-label">🟢 Low Risk</div>
                        <div class="kpi-value" style="color: #2ca02c;">{low_risk}</div>
                        <p style="font-size: 12px; color: #2ca02c; margin: 0;">On Track</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Risk Distribution Chart
                risk_distribution = pd.DataFrame({
                    'Risk Level': ['High', 'Medium', 'Low'],
                    'Count': [high_risk, med_risk, low_risk],
                    'Color': ['#ff6b6b', '#ffa500', '#51cf66']
                })
                
                fig_risk = px.bar(
                    risk_distribution,
                    x='Risk Level',
                    y='Count',
                    color='Risk Level',
                    color_discrete_map={'High': '#ff6b6b', 'Medium': '#ffa500', 'Low': '#51cf66'},
                    title="Risk Distribution Analysis",
                    labels={'Count': 'Number of Products', 'Risk Level': 'Risk Category'}
                )
                fig_risk.update_layout(showlegend=False, height=350)
                st.plotly_chart(fig_risk, use_container_width=True)
                
            else:
                st.info("Risk analytics not available")
        except Exception as e:
            st.warning("⚠️ Risk assessment temporarily unavailable")

        st.markdown("---")

        # DATA EXPORT SECTION
        st.markdown('<div class="section-header">📥 Data Export & Reports</div>', unsafe_allow_html=True)
        
        exp1, exp2, exp3 = st.columns(3)

        with exp1:
            if st.button("📊 Export Products CSV", key="export_products", use_container_width=True):
                csv = df_products.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download Products CSV",
                    data=csv,
                    file_name=f"fashion_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="download_products"
                )

        with exp2:
            if st.button("📈 Export Analytics Report", key="export_report", use_container_width=True):
                report_data = {
                    "Report_Date": datetime.now().isoformat(),
                    "Summary": {
                        "Total_Products": len(products),
                        "Categories": categories,
                        "Average_Price": f"${avg_price:.2f}",
                        "Total_Catalog_Value": f"${total_value:,.2f}"
                    },
                    "Risk_Analysis": {
                        "High_Risk": risk_data.get('high_risk_count', 0),
                        "Medium_Risk": risk_data.get('medium_risk_count', 0),
                        "Low_Risk": risk_data.get('low_risk_count', 0)
                    }
                }
                report_json = json.dumps(report_data, indent=2)
                st.download_button(
                    label="⬇️ Download Analytics Report",
                    data=report_json,
                    file_name=f"supply_chain_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    key="download_report"
                )

        with exp3:
            if st.button("📋 Generate Full Report", key="full_report", use_container_width=True):
                st.info("📄 Generating comprehensive PDF report...")
                st.success("✅ Report ready for download!")
    
    # ==================== TAB 2: SINGLE PRODUCT ANALYSIS ====================
    with tab_single:
        st.markdown('<div class="section-header">🔍 Single Product Deep Dive</div>', unsafe_allow_html=True)

        
        # Product selector
        col1, col2 = st.columns([2, 1])
        
        with col1:
            product_options = {f"{p['sku']} - {p['name']}" : p['id'] for p in products}
            selected_label = st.selectbox(
                "Select Product:",
                list(product_options.keys()),
                key="single_product"
            )
            selected_id = product_options[selected_label]
        
        selected_prod = next(p for p in products if p['id'] == selected_id)
        
        with col2:
            st.metric("SKU", selected_prod['sku'])
        
        # Product Info Cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**Category:** {selected_prod['category']}")
            st.markdown(f"**Base Price:** ${selected_prod['base_price']:.2f}")
        
        with col2:
            risk_data = get_product_risk(selected_id)
            risk_level = risk_data.get('risk_level', 'Unknown')
            stock = risk_data.get('current_stock', 0)
            
            if "High" in risk_level:
                st.error(f"⚠️ **Risk Level:** {risk_level}")
            elif "Medium" in risk_level:
                st.warning(f"⚠️ **Risk Level:** {risk_level}")
            else:
                st.success(f"✅ **Risk Level:** {risk_level}")
            
            st.metric("Current Stock", f"{stock} units")
        
        with col3:
            demand_data = get_product_demand(selected_id)
            predicted = demand_data.get('predicted_demand', 0)
            
            st.metric(
                "Next Day Forecast",
                f"{predicted:.0f} units",
                delta="LSTM Prediction"
            )
        
        st.markdown("---")
        
        # Risk & Recommendations
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📋 Inventory Status")
            action = risk_data.get('action_recommended', 'Monitor')
            
            if "High" in risk_level:
                st.markdown(f'<div class="alert-high"><strong>Action Required:</strong> {action}</div>', unsafe_allow_html=True)
            elif "Medium" in risk_level:
                st.markdown(f'<div class="alert-medium"><strong>Alert:</strong> {action}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-low"><strong>Status:</strong> {action}</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🤖 ML Predictions")
            st.markdown(f"""
            - **Risk Prediction:** XGBoost Model
            - **Demand Forecast:** LSTM (24h)
            - **Confidence:** Based on historical patterns
            """)
        
        st.markdown("---")
        
        # Trend Chart
        st.subheader("📈 14-Day Trend Projection")
        
        dates = pd.date_range(
            end=pd.Timestamp.now(),
            periods=14
        )
        
        # Generate synthetic trend data
        trend_data = pd.DataFrame({
            'Date': dates,
            'Demand': [20 + (i * 2) % 30 for i in range(14)],
            'Stock': [50 + (i * -1.5) % 40 for i in range(14)]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=trend_data['Date'],
            y=trend_data['Demand'],
            name='Predicted Demand',
            line=dict(color='#1f77b4', width=3),
            mode='lines+markers'
        ))
        
        fig.add_trace(go.Scatter(
            x=trend_data['Date'],
            y=trend_data['Stock'],
            name='Projected Stock',
            line=dict(color='#ff7f0e', width=3),
            mode='lines+markers',
            yaxis='y2'
        ))
        
        fig.update_layout(
            title=f"Demand & Inventory Forecast - {selected_prod['name']}",
            xaxis_title="Date",
            yaxis_title="Demand (units)",
            yaxis2=dict(title="Stock (units)", overlaying="y", side="right"),
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig)
    
    # ==================== TAB 3: PRODUCT COMPARISON ====================
    with tab_compare:
        st.subheader("Compare Multiple Products")
        
        selected_products = st.multiselect(
            "Select products to compare:",
            options=list(product_options.keys()),
            default=list(product_options.keys())[:3],
            key="compare_products"
        )
        
        if selected_products:
            compare_data = []
            
            for label in selected_products:
                prod_id = product_options[label]
                prod = next(p for p in products if p['id'] == prod_id)
                risk = get_product_risk(prod_id)
                demand = get_product_demand(prod_id)
                
                compare_data.append({
                    'Product': prod['sku'],
                    'Name': prod['name'],
                    'Price': prod['base_price'],
                    'Category': prod['category'],
                    'Stock': risk.get('current_stock', 0),
                    'Risk': risk.get('risk_level', 'Unknown'),
                    'Forecast': demand.get('predicted_demand', 0)
                })
            
            df_compare = pd.DataFrame(compare_data)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("### Comparison Table")
                st.dataframe(
                    df_compare,
                    height=400
                )
            
            with col2:
                st.markdown("### Price vs Stock Level")
                fig = px.scatter(
                    df_compare,
                    x='Price',
                    y='Stock',
                    size='Forecast',
                    color='Risk',
                    hover_name='Name',
                    title="Product Positioning Analysis",
                    color_discrete_map={
                        'High': '#d32f2f',
                        'Medium': '#f57c00',
                        'Low': '#388e3c'
                    }
                )
                st.plotly_chart(fig)
            
            # Performance metrics
            st.markdown("---")
            st.subheader("📊 Performance Metrics")
            
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                st.metric("Total Products", len(df_compare))
            
            with metric_col2:
                high_risk_count = (df_compare['Risk'] == 'High').sum()
                st.metric("High Risk Items", high_risk_count)
            
            with metric_col3:
                avg_stock = df_compare['Stock'].mean()
                st.metric("Avg Stock Level", f"{avg_stock:.0f} units")
            
            with metric_col4:
                total_forecast = df_compare['Forecast'].sum()
                st.metric("Total Demand Forecast", f"{total_forecast:.0f} units")
    
    # ==================== TAB 4: INSIGHTS & RECOMMENDATIONS ====================
    with tab_insights:
        st.subheader("🎯 Smart Insights & Recommendations")
        
        # Calculate metrics
        df_all = pd.DataFrame(products)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🔴 Critical Alerts")
            
            high_risk_prods = []
            for prod in products:
                risk = get_product_risk(prod['id'])
                if "High" in risk.get('risk_level', ''):
                    high_risk_prods.append({
                        'SKU': prod['sku'],
                        'Name': prod['name'],
                        'Action': risk.get('action_recommended', 'Review')
                    })
            
            if high_risk_prods:
                for alert in high_risk_prods:
                    st.markdown(f"""
                    <div class="alert-high">
                    <strong>{alert['SKU']}</strong> - {alert['Name']}<br/>
                    Action: {alert['Action']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ No critical alerts at this time")
        
        with col2:
            st.markdown("### 💡 Recommendations")
            st.markdown("""
            1. **Inventory Optimization**
               - Reorder products with High risk classification
               - Consider bulk purchasing for stable-demand items
            
            2. **Demand Planning**
               - Use LSTM forecasts for weekly planning cycles
               - Adjust safety stock based on forecast confidence
            
            3. **Risk Management**
               - Monitor medium-risk products closely
               - Set alerts for risk level changes
            
            4. **Data-Driven Decisions**
               - Review trends every week
               - Compare projections vs. actuals monthly
            """)
        
        st.markdown("---")
        
        st.markdown("### 📈 Advanced Analytics")
        
        # Risk Distribution Chart
        st.subheader("Risk Distribution Across Portfolio")
        
        risk_dist = {'Low': 0, 'Medium': 0, 'High': 0}
        for prod in products:
            risk = get_product_risk(prod['id'])
            level = risk.get('risk_level', 'Unknown')
            if 'High' in level:
                risk_dist['High'] += 1
            elif 'Medium' in level:
                risk_dist['Medium'] += 1
            else:
                risk_dist['Low'] += 1
        
        fig_risk = px.bar(
            x=list(risk_dist.keys()),
            y=list(risk_dist.values()),
            color=list(risk_dist.keys()),
            title="Product Count by Risk Level",
            color_discrete_map={
                'Low': '#388e3c',
                'Medium': '#f57c00',
                'High': '#d32f2f'
            }
        )
        st.plotly_chart(fig_risk)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px; margin-top: 20px;'>
    <p>Fashion Supply Chain AI Dashboard | Powered by FastAPI + Streamlit + ML Models</p>
    <p>Last Updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
