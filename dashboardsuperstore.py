import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------- CONFIG PAGE -----------------------
st.set_page_config(page_title="Superstore Analytics Dashboard", layout="wide", page_icon="📊")

# ----------------------- LOAD DATA ------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('superstore_order.xlsx')
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
        
        numeric_cols = ['sales', 'profit', 'quantity', 'discount']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        date_cols = ['order_date', 'ship_date']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        st.sidebar.success(f"✅ Data loaded: {len(df):,} records")
        st.sidebar.info(f"📋 Columns: {len(df.columns)}")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()
if df is None:
    st.stop()

# ----------------------- DASHBOARD HEADER -----------------------
st.title("📊 Superstore Analytics Dashboard")
st.markdown("---")

# ----------------------- SIDEBAR NAVIGATION -----------------------
st.sidebar.header("Dashboard Navigation")
view_option = st.sidebar.radio(
    "Pilih Analisis:",
    ["Overview", "Sales Analysis", "Profit & Margin", "Customer Analysis",
     "Product Analysis", "Shipping Performance", "Time Series Analysis"]
)

# ======================= OVERVIEW =======================
if view_option == "Overview":
    st.header("📈 Business Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    total_sales = df['sales'].sum()
    total_profit = df['profit'].sum()
    total_orders = df['order_id'].nunique()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Total Orders", f"{total_orders:,}")
    col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")
    
    st.markdown("---")
    
    # Sales by Region
    if 'region' in df.columns:
        region_sales = df.groupby('region')['sales'].sum().reset_index()
        fig1 = px.pie(region_sales, values='sales', names='region',
                      title='Sales by Region', color_discrete_sequence=px.colors.sequential.Teal)
        fig1.update_layout(title_font_size=24)
        st.plotly_chart(fig1, width='stretch')
    
    # Shipping performance overview
    if 'ship_mode' in df.columns and 'order_date' in df.columns and 'ship_date' in df.columns:
        df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days
        shipping_summary = df.groupby('ship_mode').agg({'order_id':'count', 'shipping_days':'mean'}).reset_index()
        shipping_summary.columns = ['ship_mode', 'total_orders', 'avg_shipping_days']
        
        col1, col2 = st.columns(2)
        with col1:
            fig2 = px.bar(shipping_summary, x='ship_mode', y='avg_shipping_days',
                          color='avg_shipping_days', color_continuous_scale='Teal',
                          title='Average Shipping Days', text='avg_shipping_days')
            fig2.update_traces(texttemplate='%{text:.1f} days', textposition='outside')
            fig2.update_layout(title_font_size=24)
            st.plotly_chart(fig2, width='stretch')
        with col2:
            fig3 = px.pie(shipping_summary, values='total_orders', names='ship_mode',
                          title='Order Distribution by Shipping Mode',
                          color_discrete_sequence=px.colors.sequential.Teal)
            fig3.update_layout(title_font_size=24)
            st.plotly_chart(fig3, width='stretch')

# ======================= SALES ANALYSIS =======================
elif view_option == "Sales Analysis":
    st.header("💼 Sales Analysis")
    
    if 'product_name' in df.columns:
        # Top 10 products by sales
        top_sales = df.groupby('product_name')['sales'].sum().sort_values(ascending=False).head(10).reset_index()
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.bar(top_sales, x='sales', y='product_name', orientation='h',
                          color='sales', color_continuous_scale='Teal',
                          title='Top 10 Products by Sales')
            fig1.update_layout(yaxis={'categoryorder':'total ascending'}, title_font_size=24)
            st.plotly_chart(fig1, width='stretch')
        
        # Sales vs Profit scatter
        prod_summary = df.groupby('product_name').agg({'sales':'sum','profit':'sum'}).reset_index()
        prod_summary['profit_margin'] = (prod_summary['profit']/prod_summary['sales']*100).fillna(0)
        top_scatter = prod_summary.sort_values('sales', ascending=False).head(50)
        
        with col2:
            fig2 = px.scatter(top_scatter, x='sales', y='profit', size='sales',
                              color='profit_margin',
                              color_continuous_scale='Teal',
                              hover_data=['product_name'], title='Sales vs Profit (Top 50 Products)')
            fig2.update_layout(title_font_size=24)
            st.plotly_chart(fig2, width='stretch')
        
        # Discount impact
        if 'discount' in df.columns:
            discount_df = df.groupby('product_name').agg({'discount':'mean','profit':'mean'}).reset_index()
            discount_df.columns = ['product_name','avg_discount','avg_profit']
            discount_df['avg_discount'] = (discount_df['avg_discount']*100).round(2)
            discount_df = discount_df.sort_values('avg_profit', ascending=False).head(15)
            
            st.subheader("Discount vs Profit")
            fig3 = px.scatter(discount_df, x='avg_discount', y='avg_profit',
                              hover_data=['product_name'], color='avg_profit',
                              color_continuous_scale='Teal',
                              labels={'avg_discount':'Avg Discount (%)','avg_profit':'Avg Profit ($)'},
                              title='Discount Impact on Profit')
            fig3.update_layout(title_font_size=24)
            st.plotly_chart(fig3, width='stretch')
            
            # Histogram shipping days
            if 'shipping_days' in df.columns:
                st.subheader("⏱️ Shipping Days Distribution")
                fig4 = px.histogram(df, x='shipping_days', nbins=20, 
                                    color_discrete_sequence=px.colors.sequential.Teal,
                                    title='Shipping Days Distribution')
                fig4.update_layout(title_font_size=24)
                st.plotly_chart(fig4, width='stretch')

# ======================= PROFIT & MARGIN =======================
elif view_option == "Profit & Margin":
    st.header("📊 Profit & Margin Analysis")
    
    if 'product_name' in df.columns:
        prod_summary = df.groupby('product_name').agg({'sales':'sum','profit':'sum','quantity':'sum'}).reset_index()
        prod_summary['profit_margin'] = (prod_summary['profit']/prod_summary['sales']*100).round(2)
        top_profit = prod_summary.sort_values('profit', ascending=False).head(15)
        
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.bar(top_profit, x='product_name', y='profit',
                          color='profit', color_continuous_scale='Teal',
                          title='Top 15 Products by Profit')
            fig1.update_layout(xaxis_tickangle=-45, title_font_size=24)
            st.plotly_chart(fig1, width='stretch')
        
        with col2:
            fig2 = px.scatter(top_profit, x='quantity', y='profit_margin',
                              hover_data=['product_name'], color='profit_margin',
                              color_continuous_scale='Teal',
                              title='Profit Margin vs Quantity Sold')
            fig2.update_layout(title_font_size=24)
            st.plotly_chart(fig2, width='stretch')

# ======================= CUSTOMER ANALYSIS =======================
elif view_option == "Customer Analysis":
    st.header("👥 Customer Analysis")
    
    if 'customer_name' in df.columns:
        cust_df = df.groupby('customer_name').agg({'order_id':'nunique','sales':'sum','profit':'sum'}).reset_index()
        cust_df.columns = ['customer_name','total_orders','total_sales','total_profit']
        top_cust = cust_df.sort_values('total_sales', ascending=False).head(15)
        
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.bar(top_cust, x='customer_name', y='total_sales', color='total_sales',
                          color_continuous_scale='Teal', title='Top Customers by Sales')
            fig1.update_layout(xaxis_tickangle=-45, title_font_size=24)
            st.plotly_chart(fig1, width='stretch')
        with col2:
            fig2 = px.bar(top_cust, x='customer_name', y='total_orders', color='total_orders',
                          color_continuous_scale='Teal', title='Top Customers by Orders')
            fig2.update_layout(xaxis_tickangle=-45, title_font_size=24)
            st.plotly_chart(fig2, width='stretch')

# ======================= PRODUCT ANALYSIS =======================
elif view_option == "Product Analysis":
    st.header("📦 Product Analysis")
    
    if 'product_name' in df.columns:
        prod_df = df.groupby('product_name').agg({'quantity':'sum','sales':'sum','profit':'sum'}).reset_index()
        prod_df.columns = ['product_name','total_quantity','total_sales','total_profit']
        top_prod = prod_df.sort_values('total_sales', ascending=False).head(20)
        
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.bar(top_prod, x='product_name', y='total_quantity', color='total_quantity',
                          color_continuous_scale='Teal', title='Top Products by Quantity Sold')
            fig1.update_layout(xaxis_tickangle=-45, title_font_size=24)
            st.plotly_chart(fig1, width='stretch')
        
        with col2:
            if 'discount' in df.columns:
                disc_df = df.groupby('product_name').agg({'discount':'mean','profit':'mean'}).reset_index()
                disc_df.columns = ['product_name','avg_discount','avg_profit']
                disc_df['avg_discount'] = (disc_df['avg_discount']*100).round(2)
                disc_df = disc_df.sort_values('avg_profit', ascending=False).head(15)
                fig2 = px.scatter(disc_df, x='avg_discount', y='avg_profit', hover_data=['product_name'],
                                  color='avg_profit', color_continuous_scale='Teal',
                                  title='Discount Impact on Profit')
                fig2.update_layout(title_font_size=24)
                st.plotly_chart(fig2, width='stretch')

# ======================= SHIPPING PERFORMANCE =======================
elif view_option == "Shipping Performance":
    st.header("🚚 Shipping Performance")
    
    if 'ship_mode' in df.columns and 'order_date' in df.columns and 'ship_date' in df.columns:
        df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days
        ship_df = df.groupby('ship_mode').agg({'order_id':'count','shipping_days':'mean','sales':'sum'}).reset_index()
        ship_df.columns = ['ship_mode','total_orders','avg_shipping_days','total_sales']
        
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.bar(ship_df, x='ship_mode', y='avg_shipping_days', color='avg_shipping_days',
                          color_continuous_scale='Teal', title='Average Shipping Days', text='avg_shipping_days')
            fig1.update_traces(texttemplate='%{text:.1f} days', textposition='outside')
            fig1.update_layout(title_font_size=24)
            st.plotly_chart(fig1, width='stretch')
        with col2:
            fig2 = px.pie(ship_df, values='total_orders', names='ship_mode', color_discrete_sequence=px.colors.sequential.Teal,
                          title='Order Distribution by Shipping Mode')
            fig2.update_layout(title_font_size=24)
            st.plotly_chart(fig2, width='stretch')
        
        fig3 = px.bar(ship_df, x='ship_mode', y='total_sales', color='total_sales',
                      color_continuous_scale='Teal', title='Revenue by Shipping Mode')
        fig3.update_layout(title_font_size=24)
        st.plotly_chart(fig3, width='stretch')

# ======================= TIME SERIES ANALYSIS =======================
elif view_option == "Time Series Analysis":
    st.header("📅 Time Series Analysis")
    
    if 'order_date' in df.columns:
        df['year_month'] = df['order_date'].dt.to_period('M').astype(str)
        ts_df = df.groupby('year_month').agg({'sales':'sum','profit':'sum','order_id':'nunique'}).reset_index()
        ts_df.columns = ['month','total_sales','total_profit','total_orders']
        ts_df['profit_margin'] = (ts_df['total_profit']/ts_df['total_sales']*100).round(2)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=ts_df['month'], y=ts_df['total_sales'],
                                  mode='lines+markers', name='Sales',
                                  line=dict(color='teal', width=2)))
        fig1.add_trace(go.Scatter(x=ts_df['month'], y=ts_df['total_profit'],
                                  mode='lines+markers', name='Profit',
                                  line=dict(color='darkcyan', width=2)))
        fig1.update_layout(title='Sales & Profit Over Time',
                          xaxis_title='Month',
                          yaxis_title='Amount ($)',
                          title_font_size=24,
                          hovermode='x unified')
        st.plotly_chart(fig1, width='stretch')
        
        fig2 = px.line(ts_df, x='month', y='profit_margin', markers=True,
                       title='Profit Margin Trend (%)', color_discrete_sequence=['teal'])
        fig2.update_layout(title_font_size=24)
        st.plotly_chart(fig2, width='stretch')

# ----------------------- FOOTER -----------------------
st.markdown("---")
st.markdown("Dashboard created with Streamlit & Plotly | Data: Superstore Analytics")
