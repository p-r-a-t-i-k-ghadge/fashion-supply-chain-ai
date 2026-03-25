import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import numpy as np
import os
import sys
from pathlib import Path

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Fashion Retail Intelligence - Business Analytics",
    layout="wide",
    page_icon="👗",
    initial_sidebar_state="expanded"
)

# ==================== HELPER FUNCTIONS ====================
@st.cache_data(ttl=300)
def generate_business_data():
    """Generate realistic fashion retail business data"""
    np.random.seed(42)
    
    days = 30
    dates = pd.date_range(end=datetime.now(), periods=days)
    
    daily_sales = np.random.randint(100000, 500000, days)
    daily_customers = np.random.randint(50, 200, days)
    daily_orders = np.random.randint(40, 150, days)
    
    categories = ['T-Shirts', 'Jeans', 'Dresses', 'Jackets', 'Accessories', 'Shoes']
    category_sales = {cat: np.random.randint(50000, 300000) for cat in categories}
    category_units = {cat: np.random.randint(20, 150) for cat in categories}
    
    return {
        'dates': dates,
        'daily_sales': daily_sales,
        'daily_customers': daily_customers,
        'daily_orders': daily_orders,
        'category_sales': category_sales,
        'category_units': category_units,
        'repeat_customers': np.random.randint(300, 800),
        'new_customers': np.random.randint(100, 400),
        'churn_rate': np.random.uniform(5, 15),
        'avg_order_value': np.random.randint(1500, 4500),
        'customer_satisfaction': np.random.uniform(4.0, 4.8),
        'return_rate': np.random.uniform(2, 8),
    }

def load_data_from_database():
    """Load data from uploaded CSV files in database"""
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from db.database import SessionLocal
        from db.models import Product, Sale, Inventory
        
        db = SessionLocal()
        
        products = db.query(Product).all()
        sales = db.query(Sale).all()
        inventory = db.query(Inventory).all()
        
        db.close()
        
        if not products:
            return None
        
        # Convert to dataframes
        products_df = pd.DataFrame([
            {'id': p.id, 'sku': p.sku, 'name': p.name, 'category': p.category, 'base_price': p.base_price}
            for p in products
        ])
        
        sales_df = pd.DataFrame([
            {'product_id': s.product_id, 'date': s.date, 'quantity': s.quantity, 'total_amount': s.total_amount}
            for s in sales
        ]) if sales else None
        
        inventory_df = pd.DataFrame([
            {'product_id': i.product_id, 'date': i.date, 'stock_level': i.stock_level, 'reorder_point': i.reorder_point, 'lead_time_days': i.lead_time_days}
            for i in inventory
        ]) if inventory else None
        
        return {'products': products_df, 'sales': sales_df, 'inventory': inventory_df}
    
    except Exception as e:
        print(f"Error loading from database: {e}")
        return None

def generate_analytics_from_data(data):
    """Generate analytics from uploaded data"""
    products_df = data['products']
    sales_df = data['sales']
    inventory_df = data['inventory']
    
    # Calculate analytics
    if sales_df is not None and len(sales_df) > 0:
        total_sales = sales_df['total_amount'].sum()
        total_quantity = sales_df['quantity'].sum()
        avg_order_value = sales_df.groupby(['product_id', 'date'])['total_amount'].sum().mean()
        total_orders = len(sales_df.groupby(['product_id', 'date']))
        
        # Daily data
        sales_df['date'] = pd.to_datetime(sales_df['date'])
        daily_data = sales_df.groupby('date').agg({
            'total_amount': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        # Category-wise
        product_sales = sales_df.merge(products_df, left_on='product_id', right_on='id')
        category_sales = product_sales.groupby('category')['total_amount'].sum().to_dict()
        category_units = product_sales.groupby('category')['quantity'].sum().to_dict()
        
    else:
        return None
    
    if inventory_df is not None and len(inventory_df) > 0:
        total_inventory = inventory_df.groupby('product_id')['stock_level'].last().sum()
        low_stock = len(inventory_df[inventory_df['stock_level'] <= inventory_df['reorder_point']])
    else:
        total_inventory = 0
        low_stock = 0
    
    return {
        'dates': daily_data['date'] if len(daily_data) > 0 else pd.date_range(end=datetime.now(), periods=1),
        'daily_sales': daily_data['total_amount'].values if len(daily_data) > 0 else [total_sales],
        'daily_customers': np.random.randint(50, 200, len(daily_data)) if len(daily_data) > 0 else [100],
        'daily_orders': daily_data['quantity'].values if len(daily_data) > 0 else [total_quantity],
        'category_sales': category_sales,
        'category_units': category_units,
        'total_sales': total_sales,
        'total_quantity': total_quantity,
        'avg_order_value': int(avg_order_value),
        'total_inventory': total_inventory,
        'low_stock_count': low_stock,
        'products_df': products_df,
        'repeat_customers': min(len(products_df) * 2, 800),
        'new_customers': len(products_df),
        'churn_rate': 5.0,
        'customer_satisfaction': 4.6,
        'return_rate': 3.5,
    }

@st.cache_data(ttl=300)
def get_customer_segments():
    """Get customer segmentation data"""
    segments = {
        'Premium Buyers': {'count': 450, 'avg_spend': 8500, 'retention': 92},
        'Regular Buyers': {'count': 2100, 'avg_spend': 3200, 'retention': 78},
        'Budget Conscious': {'count': 3800, 'avg_spend': 1200, 'retention': 55},
        'One-time Buyers': {'count': 5200, 'avg_spend': 1800, 'retention': 0}
    }
    return segments

@st.cache_data(ttl=300)
def get_top_products():
    """Get top selling products"""
    products = [
        {'name': 'Premium Cotton T-Shirt', 'sales': 850000, 'units': 450, 'rating': 4.8, 'category': 'T-Shirts'},
        {'name': 'Slim Fit Jeans', 'sales': 720000, 'units': 320, 'rating': 4.6, 'category': 'Jeans'},
        {'name': 'Summer Dress', 'sales': 650000, 'units': 280, 'rating': 4.7, 'category': 'Dresses'},
        {'name': 'Leather Jacket', 'sales': 580000, 'units': 150, 'rating': 4.5, 'category': 'Jackets'},
        {'name': 'Sports Shoes', 'sales': 520000, 'units': 220, 'rating': 4.4, 'category': 'Shoes'}
    ]
    return pd.DataFrame(products)

def process_uploaded_data(df_products, df_sales=None, df_inventory=None):
    """Process and save uploaded CSV data to database"""
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from db.database import SessionLocal, engine, Base
        from db.models import Product, Sale, Inventory

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
                except Exception as e:
                    print(f"Error processing sales row: {e}")
                    continue

        # Process inventory data
        if df_inventory is not None:
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
                except Exception as e:
                    print(f"Error processing inventory row: {e}")
                    continue

        db.commit()
        db.close()
        return True

    except Exception as e:
        print(f"Error in process_uploaded_data: {e}")
        return False

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
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
    
    .section-header {
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
        margin-bottom: 20px;
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }
    
    .alert-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        border-left: 6px solid #d62728;
        padding: 15px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
    }
    
    .success-box {
        background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        border-left: 6px solid #2ca02c;
        padding: 15px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div style="text-align: center; padding: 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin-bottom: 30px;">
    <h1 style="font-size: 3em; margin: 0;">👗 Fashion Retail Intelligence</h1>
    <p style="font-size: 1.2em; margin: 10px 0;">AI-Powered Business Analytics for Fashion Sellers 🇮🇳</p>
    <p style="font-size: 0.95em; opacity: 0.9;">💰 Revenue • 👥 Customer Behavior • 📊 Sales Trends • 📦 Inventory • 💡 Recommendations • All in ₹ INR</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col2:
    st.caption("🟢 Live Intelligence Platform • Updated: " + datetime.now().strftime("%d-%b %H:%M"))

# ==================== SIDEBAR: DATA MANAGEMENT ====================
with st.sidebar:
    st.header("⚙️ Data Management")
    
    data_tab1, data_tab2 = st.tabs(["Generate Data", "Upload Data"])
    
    with data_tab1:
        st.markdown("### 📊 Synthetic Data")
        if st.button("🔄 Generate Sample Data", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ Sample data loaded!")
            st.rerun()
    
    with data_tab2:
        st.markdown("### 📤 Your Own Data")
        
        products_file = st.file_uploader(
            "📦 Products CSV",
            type=['csv'],
            help="sku, name, category, base_price"
        )
        
        sales_file = st.file_uploader(
            "💰 Sales CSV",
            type=['csv'],
            help="sku, date, quantity, total_amount"
        )
        
        inventory_file = st.file_uploader(
            "📦 Inventory CSV",
            type=['csv'],
            help="sku, date, stock_level, reorder_point, lead_time_days"
        )
        
        if st.button("📤 Upload to Database", use_container_width=True):
            if not products_file:
                st.error("❌ Products file required")
            else:
                try:
                    with st.spinner("⏳ Processing..."):
                        df_products = pd.read_csv(products_file)
                        df_sales = pd.read_csv(sales_file) if sales_file else None
                        df_inventory = pd.read_csv(inventory_file) if inventory_file else None
                        
                        success = process_uploaded_data(df_products, df_sales, df_inventory)
                        
                        if success:
                            st.success("✅ Data uploaded!")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error("❌ Upload failed")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ==================== MAIN TABS ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Sales Dashboard",
    "👥 Customer Insights",
    "🛍️ Top Products",
    "💡 AI Recommendations",
    "📦 Inventory Status"
])

# Load data - First try database, then fallback to mock data
db_data = load_data_from_database()

if db_data is not None:
    st.sidebar.info("✅ Using uploaded CSV data")
    biz_data = generate_analytics_from_data(db_data)
    if biz_data is None:
        # Fallback to mock if analysis fails
        biz_data = generate_business_data()
        st.sidebar.warning("⚠️ Fallback to sample data")
else:
    st.sidebar.info("📊 Using sample data (upload CSV to replace)")
    biz_data = generate_business_data()

segments = get_customer_segments()
top_products = get_top_products()

# ==================== TAB 1: SALES DASHBOARD ====================
with tab1:
    st.markdown('<div class="section-header">📊 Revenue & Sales Performance</div>', unsafe_allow_html=True)
    
    total_sales = biz_data['daily_sales'].sum()
    total_orders = biz_data['daily_orders'].sum()
    total_customers = biz_data['daily_customers'].sum()
    avg_order_value = biz_data['avg_order_value']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">💰 Total Revenue</div>
            <div class="kpi-value">₹{total_sales/100000:.2f}L</div>
            <p style="font-size: 12px; color: #2ca02c; margin: 0;">📈 +12.5% vs Last Month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📦 Total Orders</div>
            <div class="kpi-value">{total_orders}</div>
            <p style="font-size: 12px; color: #2ca02c; margin: 0;">🎯 +8.3% vs Last Month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">👥 Customers</div>
            <div class="kpi-value">{total_customers}</div>
            <p style="font-size: 12px; color: #2ca02c; margin: 0;">✅ Active This Month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">💵 Avg Order Value</div>
            <div class="kpi-value">₹{avg_order_value:,}</div>
            <p style="font-size: 12px; color: #667eea; margin: 0;">Basket Size</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Daily Revenue Trend")
        
        # Handle both array and series data
        sales_data = biz_data['daily_sales']
        if isinstance(sales_data, np.ndarray):
            sales_values = sales_data
        else:
            sales_values = sales_data.values if hasattr(sales_data, 'values') else sales_data
        
        dates_data = biz_data['dates']
        if isinstance(dates_data, pd.DatetimeIndex):
            dates_values = dates_data
        else:
            dates_values = dates_data.values if hasattr(dates_data, 'values') else dates_data
        
        fig_sales = go.Figure()
        fig_sales.add_trace(go.Scatter(
            x=dates_values,
            y=sales_values,
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.2)',
            line=dict(color='#667eea', width=3),
            name='Daily Sales'
        ))
        fig_sales.update_layout(
            height=350,
            hovermode='x unified',
            template='plotly_white',
            xaxis_title='Date',
            yaxis_title='Revenue (₹)'
        )
        fig_sales.update_yaxes(tickprefix='₹')
        st.plotly_chart(fig_sales, use_container_width=True)
    
    with col2:
        st.markdown("### 📦 Orders vs Customers")
        
        orders_data = biz_data['daily_orders']
        if isinstance(orders_data, np.ndarray):
            orders_values = orders_data
        else:
            orders_values = orders_data.values if hasattr(orders_data, 'values') else orders_data
        
        customers_data = biz_data['daily_customers']
        if isinstance(customers_data, np.ndarray):
            customers_values = customers_data
        else:
            customers_values = customers_data.values if hasattr(customers_data, 'values') else customers_data
        
        fig_orders = go.Figure()
        fig_orders.add_trace(go.Bar(
            x=dates_values,
            y=orders_values,
            name='Orders',
            marker_color='rgb(255, 127, 14)'
        ))
        fig_orders.add_trace(go.Scatter(
            x=dates_values,
            y=customers_values,
            name='Customers',
            line=dict(color='#2ca02c', width=2),
            yaxis='y2'
        ))
        fig_orders.update_layout(
            height=350,
            hovermode='x unified',
            yaxis=dict(title='Orders'),
            yaxis2=dict(title='Customers', overlaying='y', side='right'),
            template='plotly_white'
        )
        st.plotly_chart(fig_orders, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 📂 Revenue by Category")
    category_df = pd.DataFrame(
        list(biz_data['category_sales'].items()),
        columns=['Category', 'Sales']
    ).sort_values('Sales', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_cat = px.bar(
            category_df,
            x='Category',
            y='Sales',
            color='Sales',
            color_continuous_scale='Blues',
            title='Revenue by Category',
            labels={'Sales': '₹ Revenue'}
        )
        fig_cat.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig_cat, use_container_width=True)
    
    with col2:
        st.markdown("**Top Categories**")
        for idx, row in category_df.iterrows():
            units = biz_data['category_units'].get(row['Category'], 0)
            avg = row['Sales'] / units if units > 0 else 0
            st.metric(
                f"🏷️ {row['Category']}",
                f"₹{row['Sales']:,.0f}",
                f"{units} units"
            )

# ==================== TAB 2: CUSTOMER INTELLIGENCE ====================
with tab2:
    st.markdown('<div class="section-header">👥 Customer Behavior & Segmentation</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Customer Segments")
        segments_df = pd.DataFrame(segments).T.reset_index()
        segments_df.columns = ['Segment', 'Count', 'Avg Spend', 'Retention %']
        st.dataframe(segments_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 📊 Segment Distribution")
        segment_sizes = [v['count'] for v in segments.values()]
        segment_names = list(segments.keys())
        
        fig_seg = px.pie(
            names=segment_names,
            values=segment_sizes,
            title='Customer Breakdown',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_seg.update_traces(textposition='inside', textinfo='label+percent')
        st.plotly_chart(fig_seg, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        repeat = biz_data['repeat_customers']
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">🔄 Repeat Customers</div>
            <div class="kpi-value">{repeat}</div>
            <p style="font-size: 12px; color: #2ca02c; margin: 0;">High Value</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        new = biz_data['new_customers']
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">✨ New Customers</div>
            <div class="kpi-value">{new}</div>
            <p style="font-size: 12px; color: #667eea; margin: 0;">This Month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        churn = biz_data['churn_rate']
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📉 Churn Rate</div>
            <div class="kpi-value">{churn:.1f}%</div>
            <p style="font-size: 12px; color: #ff6b6b; margin: 0;">⚠️ At Risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        satisfaction = biz_data['customer_satisfaction']
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">⭐ Satisfaction</div>
            <div class="kpi-value">{satisfaction:.1f}/5</div>
            <p style="font-size: 12px; color: #f59e0b; margin: 0;">Rating</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 3: TOP PRODUCTS ====================
with tab3:
    st.markdown('<div class="section-header">🛍️ Top Selling Products</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Top 5 Products by Revenue")
        fig_top = px.bar(
            top_products,
            x='name',
            y='sales',
            color='rating',
            color_continuous_scale='Viridis',
            title='Revenue Leaders',
            labels={'sales': '₹ Revenue', 'name': ''},
            height=350
        )
        fig_top.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Product Performance")
        for idx, row in top_products.iterrows():
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**{idx+1}. {row['name']}**")
                st.caption(f"₹{row['sales']:,} • {row['units']} units • {row['category']}")
            with col_b:
                st.metric("Rating", f"⭐{row['rating']}")

# ==================== TAB 4: AI RECOMMENDATIONS ====================
with tab4:
    st.markdown('<div class="section-header">💡 AI-Powered Business Recommendations</div>', unsafe_allow_html=True)
    
    st.markdown("### 🚀 Immediate Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="alert-box">
        🔴 URGENT: Restock Low Items
        </div>
        
        **Problem:** 8 products at risk of stockouts
        **Impact:** ₹50,000+ lost revenue
        **Action:** Reorder Jeans (45 units), T-Shirts (60 units)
        **Timeline:** 3 days
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-box">
        🟢 OPPORTUNITY: Repeat Purchase Campaign
        </div>
        
        **Insight:** 450 customers bought last 30 days
        **Opportunity:** 15% off for repeat purchase
        **Expected Revenue:** ₹3,50,000+
        **Timeline:** Launch immediately
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📈 Strategic Initiatives")
    
    st.markdown("""
    1. **Premium Tier Expansion** - New luxury collection, ₹2,00,000+/month revenue
    2. **Seasonal Campaign** - Summer collection push, 3.5x ROI expected
    3. **Churn Prevention** - Win-back program for inactive customers, ₹1,00,000 recovery
    4. **AOV Optimization** - Increase average order value from ₹2,800 → ₹3,500 (18% lift)
    """)

# ==================== TAB 5: INVENTORY STATUS ====================
with tab5:
    st.markdown('<div class="section-header">📦 Inventory & Supply Chain</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">📦 Total Stock</div>
            <div class="kpi-value">1,250 units</div>
            <p style="font-size: 12px; color: #667eea; margin: 0;">Across all SKUs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">🔔 Low Stock Items</div>
            <div class="kpi-value">8</div>
            <p style="font-size: 12px; color: #ff6b6b; margin: 0;">Need reorder</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">⚠️ Stockouts</div>
            <div class="kpi-value">2</div>
            <p style="font-size: 12px; color: #d62728; margin: 0;">Acting now</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">📊 Turnover Ratio</div>
            <div class="kpi-value">4.2x</div>
            <p style="font-size: 12px; color: #2ca02c; margin: 0;">Monthly</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🚨 Critical Alerts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.error("""
        🔴 **CRITICAL:** 2 Items Out of Stock
        - Premium Cotton T-Shirt (Best seller!)
        - Summer Dress (High demand)
        
        **Impact:** ₹75,000/day lost revenue
        **Action:** Emergency reorder from supplier
        """)
    
    with col2:
        st.warning("""
        🟡 **WARNING:** 6 Items Below Reorder Point
        - Slim Fit Jeans (25 units)
        - Leather Jacket (12 units)
        
        **Recommend:** Bulk order ₹5,00,000 stock
        **Benefit:** 10% supplier discount
        """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🇮🇳 Fashion Retail Intelligence Platform • Powered by AI • All Values in ₹ INR</p>
    <p style="font-size: 0.9em;">Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")} | Data Features: Synthetic + CSV Upload</p>
</div>
""", unsafe_allow_html=True)
