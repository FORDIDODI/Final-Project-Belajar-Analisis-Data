import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="E-Commerce Analysis Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 36px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #2ecc71;
        margin-top: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('main_data.csv')
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    return df

# Load the data
try:
    main_df = load_data()
    
    # Header
    st.markdown('<div class="main-header">🛒 E-Commerce Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("📊 Dashboard Navigation")
    page = st.sidebar.radio(
        "Select Analysis",
        ["Overview", "Delivery Performance", "RFM Segmentation", "Geospatial Analysis"]
    )
    
    # Filters
    st.sidebar.markdown("### Filters")
    
    # Date range filter
    min_date = main_df['order_purchase_timestamp'].min().date()
    max_date = main_df['order_purchase_timestamp'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data
    if len(date_range) == 2:
        filtered_df = main_df[
            (main_df['order_purchase_timestamp'].dt.date >= date_range[0]) &
            (main_df['order_purchase_timestamp'].dt.date <= date_range[1])
        ]
    else:
        filtered_df = main_df
    
    # State filter
    states = ['All'] + sorted(main_df['customer_state'].unique().tolist())
    selected_state = st.sidebar.selectbox("Select State", states)
    
    if selected_state != 'All':
        filtered_df = filtered_df[filtered_df['customer_state'] == selected_state]
    
    # PAGE: OVERVIEW
    if page == "Overview":
        st.markdown('<div class="sub-header">Business Overview</div>', unsafe_allow_html=True)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_orders = filtered_df['order_id'].nunique()
            st.metric("Total Orders", f"{total_orders:,}")
        
        with col2:
            total_customers = filtered_df['customer_unique_id'].nunique()
            st.metric("Total Customers", f"{total_customers:,}")
        
        with col3:
            total_revenue = filtered_df['total_payment'].sum()
            st.metric("Total Revenue", f"R$ {total_revenue:,.2f}")
        
        with col4:
            avg_review = filtered_df['review_score'].mean()
            st.metric("Avg Review Score", f"{avg_review:.2f} ⭐")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Orders Over Time")
            monthly_orders = filtered_df.groupby(filtered_df['order_purchase_timestamp'].dt.to_period('M'))['order_id'].nunique()
            
            fig, ax = plt.subplots(figsize=(10, 5))
            monthly_orders.plot(kind='line', ax=ax, color='#1f77b4', linewidth=2, marker='o')
            ax.set_xlabel('Month', fontweight='bold')
            ax.set_ylabel('Number of Orders', fontweight='bold')
            ax.set_title('Monthly Orders Trend', fontweight='bold', fontsize=14)
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        with col2:
            st.markdown("#### Review Score Distribution")
            review_dist = filtered_df['review_score'].value_counts().sort_index()
            
            fig, ax = plt.subplots(figsize=(10, 5))
            colors = ['#e74c3c', '#e67e22', '#f39c12', '#2ecc71', '#27ae60']
            ax.bar(review_dist.index, review_dist.values, color=colors, edgecolor='black', alpha=0.8)
            ax.set_xlabel('Review Score', fontweight='bold')
            ax.set_ylabel('Count', fontweight='bold')
            ax.set_title('Distribution of Review Scores', fontweight='bold', fontsize=14)
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
        
        # Top categories
        st.markdown("#### Top 10 Product Categories by Revenue")
        top_categories = filtered_df.groupby('product_category_name_english').agg({
            'order_id': 'nunique',
            'total_payment': 'sum'
        }).sort_values('total_payment', ascending=False).head(10)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, 10))
        ax.barh(range(10), top_categories['total_payment'], color=colors, edgecolor='black')
        ax.set_yticks(range(10))
        ax.set_yticklabels(top_categories.index)
        ax.set_xlabel('Revenue (R$)', fontweight='bold')
        ax.set_title('Top 10 Categories by Revenue', fontweight='bold', fontsize=14)
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig)
    
    # PAGE: DELIVERY PERFORMANCE
    elif page == "Delivery Performance":
        st.markdown('<div class="sub-header">🚚 Delivery Performance Analysis</div>', unsafe_allow_html=True)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_delivery = filtered_df['delivery_time_days'].mean()
            st.metric("Avg Delivery Time", f"{avg_delivery:.1f} days")
        
        with col2:
            on_time_rate = (filtered_df['is_delayed'] == False).sum() / len(filtered_df) * 100
            st.metric("On-Time Delivery Rate", f"{on_time_rate:.1f}%")
        
        with col3:
            delayed_orders = (filtered_df['is_delayed'] == True).sum()
            st.metric("Delayed Orders", f"{delayed_orders:,}")
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Review Score by Delivery Status")
            delivery_review = filtered_df.groupby('is_delayed')['review_score'].mean()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            colors = ['#2ecc71', '#e74c3c']
            bars = ax.bar(['On Time/Early', 'Delayed'], delivery_review.values, 
                         color=colors, edgecolor='black', alpha=0.8)
            ax.set_ylabel('Average Review Score', fontweight='bold')
            ax.set_title('Delivery Status Impact on Satisfaction', fontweight='bold')
            ax.set_ylim([0, 5])
            ax.axhline(y=4, color='gray', linestyle='--', alpha=0.5)
            ax.grid(axis='y', alpha=0.3)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}', ha='center', va='bottom', fontweight='bold')
            
            st.pyplot(fig)
        
        with col2:
            st.markdown("#### Satisfaction Rate by Delay Category")
            
            def categorize_delay(days):
                if days <= 0:
                    return 'On Time/Early'
                elif days <= 7:
                    return '1-7 days late'
                elif days <= 14:
                    return '8-14 days late'
                else:
                    return '>14 days late'
            
            filtered_df['delay_category'] = filtered_df['delivery_delay_days'].apply(categorize_delay)
            
            delay_cat_order = ['On Time/Early', '1-7 days late', '8-14 days late', '>14 days late']
            satisfaction_data = filtered_df.groupby('delay_category').agg({
                'is_satisfied': 'mean',
                'is_unsatisfied': 'mean'
            }).reindex(delay_cat_order) * 100
            
            fig, ax = plt.subplots(figsize=(8, 6))
            x = np.arange(len(delay_cat_order))
            width = 0.35
            
            ax.bar(x - width/2, satisfaction_data['is_satisfied'], width, 
                  label='Satisfied', color='#2ecc71', edgecolor='black', alpha=0.8)
            ax.bar(x + width/2, satisfaction_data['is_unsatisfied'], width,
                  label='Unsatisfied', color='#e74c3c', edgecolor='black', alpha=0.8)
            
            ax.set_ylabel('Percentage (%)', fontweight='bold')
            ax.set_title('Satisfaction vs Unsatisfaction by Delay', fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(delay_cat_order, rotation=15, ha='right')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            
            st.pyplot(fig)
        
        # Insights
        st.markdown("### 💡 Key Insights")
        st.info("""
        - **Delivery performance directly impacts customer satisfaction**
        - On-time deliveries receive average review of 4.21 vs 2.55 for delayed orders
        - Delays >7 days result in 75%+ dissatisfaction rate
        - **Recommendation**: Prioritize logistics optimization and proactive communication
        """)
    
    # PAGE: RFM SEGMENTATION
    elif page == "RFM Segmentation":
        st.markdown('<div class="sub-header">👥 RFM Customer Segmentation</div>', unsafe_allow_html=True)
        
        # Calculate RFM
        reference_date = filtered_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
        
        rfm_df = filtered_df.groupby('customer_unique_id').agg({
            'order_purchase_timestamp': lambda x: (reference_date - x.max()).days,
            'order_id': 'nunique',
            'total_payment': 'sum'
        }).reset_index()
        
        rfm_df.columns = ['customer_id', 'recency', 'frequency', 'monetary']
        
        # RFM Scoring
        rfm_df['r_score'] = pd.qcut(rfm_df['recency'], q=5, labels=[5, 4, 3, 2, 1])
        rfm_df['f_score'] = pd.qcut(rfm_df['frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5])
        rfm_df['m_score'] = pd.qcut(rfm_df['monetary'], q=5, labels=[1, 2, 3, 4, 5])
        
        rfm_df['rfm_score'] = (
            rfm_df['r_score'].astype(int) + 
            rfm_df['f_score'].astype(int) + 
            rfm_df['m_score'].astype(int)
        ) / 3
        
        # Segmentation
        def rfm_segment(row):
            r, f, m = int(row['r_score']), int(row['f_score']), int(row['m_score'])
            
            if r >= 4 and f >= 4 and m >= 4:
                return 'Champions'
            elif r >= 3 and f >= 4:
                return 'Loyal Customers'
            elif r >= 4 and f >= 2 and f <= 3:
                return 'Potential Loyalist'
            elif r >= 4 and f == 1:
                return 'Recent Customers'
            elif r <= 2 and f >= 3:
                return 'At Risk'
            elif r <= 2 and m >= 4:
                return "Can't Lose Them"
            elif r <= 2 and f <= 2:
                return 'Hibernating'
            else:
                return 'Need Attention'
        
        rfm_df['segment'] = rfm_df.apply(rfm_segment, axis=1)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            champions = len(rfm_df[rfm_df['segment'] == 'Champions'])
            st.metric("Champions", f"{champions:,}")
        
        with col2:
            at_risk = len(rfm_df[rfm_df['segment'] == 'At Risk'])
            st.metric("At Risk", f"{at_risk:,}")
        
        with col3:
            avg_monetary = rfm_df['monetary'].mean()
            st.metric("Avg Customer Value", f"R$ {avg_monetary:.2f}")
        
        with col4:
            avg_frequency = rfm_df['frequency'].mean()
            st.metric("Avg Purchase Frequency", f"{avg_frequency:.2f}")
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Customer Count by Segment")
            segment_counts = rfm_df['segment'].value_counts().sort_values(ascending=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = plt.cm.Set3(np.linspace(0, 1, len(segment_counts)))
            ax.barh(range(len(segment_counts)), segment_counts.values, 
                   color=colors, edgecolor='black', alpha=0.8)
            ax.set_yticks(range(len(segment_counts)))
            ax.set_yticklabels(segment_counts.index)
            ax.set_xlabel('Number of Customers', fontweight='bold')
            ax.set_title('Customer Distribution by Segment', fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            st.pyplot(fig)
        
        with col2:
            st.markdown("#### Revenue by Segment")
            segment_revenue = rfm_df.groupby('segment')['monetary'].sum().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(segment_revenue)))
            ax.bar(range(len(segment_revenue)), segment_revenue.values / 1000000,
                  color=colors, edgecolor='black', alpha=0.8)
            ax.set_xticks(range(len(segment_revenue)))
            ax.set_xticklabels(segment_revenue.index, rotation=45, ha='right')
            ax.set_ylabel('Revenue (Millions R$)', fontweight='bold')
            ax.set_title('Total Revenue by Segment', fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
        
        # Segment details
        st.markdown("### 📊 Segment Details")
        segment_summary = rfm_df.groupby('segment').agg({
            'customer_id': 'count',
            'recency': 'mean',
            'frequency': 'mean',
            'monetary': 'mean'
        }).round(2)
        segment_summary.columns = ['Count', 'Avg Recency', 'Avg Frequency', 'Avg Monetary']
        st.dataframe(segment_summary, use_container_width=True)
        
        # Insights
        st.markdown("### 💡 Key Insights")
        st.info("""
        - **Champions** (top customers): High value, recent, frequent - maintain with VIP programs
        - **At Risk** (23.8%): Former loyal customers - urgent win-back campaigns needed
        - **Potential Loyalist**: Recent buyers - nurture with onboarding programs
        - **Can't Lose Them**: High value but inactive - premium retention strategies
        """)
    
    # PAGE: GEOSPATIAL ANALYSIS
    elif page == "Geospatial Analysis":
        st.markdown('<div class="sub-header">🗺️ Geographic Distribution Analysis</div>', unsafe_allow_html=True)
        
        # State analysis
        state_analysis = filtered_df.groupby('customer_state').agg({
            'customer_unique_id': 'nunique',
            'order_id': 'nunique',
            'total_payment': 'sum'
        }).reset_index()
        
        state_analysis.columns = ['state', 'customers', 'orders', 'revenue']
        state_analysis['revenue_per_customer'] = state_analysis['revenue'] / state_analysis['customers']
        state_analysis = state_analysis.sort_values('revenue', ascending=False)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            top_state = state_analysis.iloc[0]
            st.metric("Top State", top_state['state'])
        
        with col2:
            top_revenue = top_state['revenue']
            st.metric("Top State Revenue", f"R$ {top_revenue:,.2f}")
        
        with col3:
            market_share = (top_revenue / state_analysis['revenue'].sum() * 100)
            st.metric("Market Share", f"{market_share:.1f}%")
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top 10 States by Revenue")
            top10 = state_analysis.head(10)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = plt.cm.viridis(np.linspace(0.3, 0.9, 10))
            ax.barh(range(10), top10['revenue'] / 1000000, color=colors, edgecolor='black', alpha=0.85)
            ax.set_yticks(range(10))
            ax.set_yticklabels(top10['state'])
            ax.set_xlabel('Revenue (Millions R$)', fontweight='bold')
            ax.set_title('Top 10 States by Revenue', fontweight='bold')
            ax.invert_yaxis()
            ax.grid(axis='x', alpha=0.3)
            st.pyplot(fig)
        
        with col2:
            st.markdown("#### Top 10 States by Customer Count")
            top10_cust = state_analysis.head(10)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = plt.cm.plasma(np.linspace(0.3, 0.9, 10))
            ax.barh(range(10), top10_cust['customers'], color=colors, edgecolor='black', alpha=0.85)
            ax.set_yticks(range(10))
            ax.set_yticklabels(top10_cust['state'])
            ax.set_xlabel('Number of Customers', fontweight='bold')
            ax.set_title('Top 10 States by Customers', fontweight='bold')
            ax.invert_yaxis()
            ax.grid(axis='x', alpha=0.3)
            st.pyplot(fig)
        
        # Market concentration
        st.markdown("#### 📊 Market Concentration")
        top5_share = (state_analysis.head(5)['revenue'].sum() / state_analysis['revenue'].sum() * 100)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        top10_revenue = state_analysis.head(10)
        others_revenue = state_analysis.iloc[10:]['revenue'].sum()
        
        pie_data = list(top10_revenue['revenue']) + [others_revenue]
        pie_labels = list(top10_revenue['state']) + ['Others']
        colors = plt.cm.Set3(np.linspace(0, 1, 11))
        
        wedges, texts, autotexts = ax.pie(pie_data, labels=pie_labels, autopct='%1.1f%%',
                                           colors=colors, startangle=90)
        ax.set_title('Revenue Distribution by State', fontweight='bold', fontsize=14)
        st.pyplot(fig)
        
        st.warning(f"⚠️ Top 5 states contribute **{top5_share:.1f}%** of total revenue - Geographic concentration risk!")
        
        # State table
        st.markdown("### 📋 State Performance Table")
        display_df = state_analysis[['state', 'customers', 'orders', 'revenue', 'revenue_per_customer']].copy()
        display_df['revenue'] = display_df['revenue'].apply(lambda x: f"R$ {x:,.2f}")
        display_df['revenue_per_customer'] = display_df['revenue_per_customer'].apply(lambda x: f"R$ {x:.2f}")
        display_df.columns = ['State', 'Customers', 'Orders', 'Revenue', 'Revenue/Customer']
        st.dataframe(display_df, use_container_width=True, height=400)
        
        # Insights
        st.markdown("### 💡 Key Insights")
        st.info("""
        - **SP dominates**: 37.5% market share - maintain competitive advantage
        - **Geographic concentration**: Top 5 states = 73% revenue - diversification needed
        - **Growth opportunities**: High-value states (PB, AC, AP) with low penetration
        - **Expansion strategy**: Invest in underserved North/Northeast regions
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("**Data Source**: Brazilian E-Commerce Public Dataset by Olist")
    st.markdown("**Analysis Period**: September 2016 - August 2018")

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Please ensure 'main_data.csv' is in the same directory as this dashboard file.")
