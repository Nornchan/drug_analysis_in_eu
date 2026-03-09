import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="EU Drug & Happiness Analysis", layout="wide")

st.title("💊 Does Happiness or Housing Drive Drug Use in the EU?")
st.markdown("""
Welcome to our Seminar Project Dashboard! We analyzed panel data (2011-2024) to see if economic despair (housing costs) 
or psychological well-being (World Happiness Report) correlates with cocaine consumption.
""")

# 2. Load the Data exported from R
@st.cache_data  # This caches the data so the app runs faster
def load_data():
    df = pd.read_csv("final_panel_data.csv")
    reg = pd.read_csv("regression_results.csv")
    return df, reg

panel_data, reg_results = load_data()

# 3. Create Columns for Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Regression Results (TWFE)")
    st.markdown("Here is the output from our Two-Way Fixed Effects model calculated in R:")
    # Display the regression table nicely
    st.dataframe(reg_results, use_container_width=True)
    
    # Add your academic interpretation
    if reg_results.loc[0, 'p.value'] > 0.05:
        st.success("**Conclusion:** The p-value is highly insignificant. National happiness does not drive cocaine use!")

with col2:
    st.header("2. Static Plot from R")
    # Display the exact ggplot you made in R
    st.image("happiness_vs_cocaine.png", caption="Generated via ggplot2 in R")

# 4. Bonus: Interactive Plot using Plotly!
st.header("3. Interactive Data Explorer")
st.markdown("Hover over the dots to see which country is which!")

# Recreating the scatter plot interactively in Python
fig = px.scatter(
    panel_data, 
    x="Happiness_Score", 
    y="drug_prev", 
    hover_name="Country", # This is the magic part: hovering shows the country name!
    color="Year",         # Colors the dots by year
    trendline="ols",      # Adds a simple regression line
    labels={
        "Happiness_Score": "Happiness Score (Cantril Ladder)",
        "drug_prev": "Cocaine Prevalence (%)"
    }
)
st.plotly_chart(fig, use_container_width=True)