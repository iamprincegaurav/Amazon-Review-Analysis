import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(page_title="AI Amazon Intelligence", layout="wide")

# Custom UI for a Premium Feel
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    [data-testid="stMetric"] { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .stAlert { border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('data/cleaned_amazon_reviews.csv')
    return df

try:
    df = load_data()
    
    # --- HEADER ---
    st.title("🧠 Amazon Consumer Intelligence Portal")
    st.markdown("Automated analysis of market trends and customer satisfaction metrics.")
    st.divider()

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("🎛️ Analysis Filters")
    all_brands = sorted(df['brand'].unique())
    selected_brands = st.sidebar.multiselect("Select Brands to Compare", all_brands, default=all_brands[:2])
    
    # Filter Logic
    mask = df['brand'].isin(selected_brands)
    filtered_df = df[mask]

    # --- SMART KPIs ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Reviews Analyzed", len(filtered_df))
    kpi2.metric("Market Sentiment", f"{filtered_df['reviews.rating'].mean():.2f} ⭐")
    
    pos_pct = (len(filtered_df[filtered_df['Sentiment']=='Positive']) / len(filtered_df) * 100) if len(filtered_df)>0 else 0
    kpi3.metric("Trust Score", f"{pos_pct:.1f}%")
    kpi4.metric("Active Segments", len(filtered_df['categories'].unique()))

    # --- VISUALS SECTION ---
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("📊 Sentiment Composition")
        fig_pie = px.pie(filtered_df, names='Sentiment', hole=0.6,
                         color_discrete_map={'Positive':'#00b894','Neutral':'#dfe6e9','Negative':'#d63031'})
        st.plotly_chart(fig_pie, width='stretch')

    with col_b:
        st.subheader("📈 Rating Distribution by Brand")
        fig_bar = px.bar(filtered_df.groupby('brand')['reviews.rating'].mean().reset_index(), 
                         x='brand', y='reviews.rating', color='brand', template="plotly_white")
        st.plotly_chart(fig_bar, width='stretch')

    # --- THE "HUMAN INTELLIGENCE" INSIGHT ---
    st.subheader("💡 AI Generated Strategy Report")
    with st.container():
        if pos_pct > 75:
            st.success(f"**Insight:** The current segment shows high brand loyalty. **Action:** Recommended to scale marketing for {', '.join(selected_brands)}.")
        else:
            st.error(f"**Alert:** Sentiment drop detected! Check Negative reviews for 'quality' or 'delivery' keywords.")

    # --- DATA EXPLORER ---
    with st.expander("🔍 Deep Dive: Interactive Review Explorer"):
        st.dataframe(filtered_df[['name', 'reviews.rating', 'Sentiment', 'reviews.text']], width=1500)

except Exception as e:
    st.error(f"System could not find the data: {e}")