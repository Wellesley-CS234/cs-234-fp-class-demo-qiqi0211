import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. Page Configuration ---
st.set_page_config(page_title="Olympics Search", layout="wide")
st.title("📊 Olympics Traffic Analysis & Search")
df_top = pd.read_csv("top_100_w_d.csv")

# --- 2. Load and Clean Data ---

# --- 3. Controls Layout ---
col_controls1, col_controls2 = st.columns([1, 2])

with col_controls1:
    # Toggle Switch
    show_post_olympics = st.checkbox("Include Post-Olympics Data", value=False)

with col_controls2:
    # SEARCH BAR
    search_term = st.text_input("🔍 Search Article Name (e.g., 'match', 'gold', 'sport')", "")

# --- 4. Select Data to Plot ---
if show_post_olympics:
    df_plot = df_top
    chart_title = "Traffic: Olympics vs Post-Olympics"
else:
    df_plot = df_top
    chart_title = "Traffic: Olympics Only"

# --- 5. Create Base Plot ---
# Define specific colors for the periods
color_map = {"Olympics": "#FF4B4B", "Post-Olympics": "#1F77B4"}

fig = px.line(
    df_top, 
    x="date", 
    y="pageviews", 
    title='article',
    markers=True,
    color_discrete_map=color_map,
    hover_data={"date": "|%B %d, %Y", "article": True, "pageviews": True, "Period": False}
)

# Customize tooltip format
fig.update_traces(
    hovertemplate="<b>%{customdata[1]}</b><br>Date: %{x|%b %d}<br>Views: %{y:,}"
)

# --- 6. Search Highlight Logic ---
matches = pd.DataFrame()

if search_term:
    # Case-insensitive search
    matches = df_top[df_top["article"].str.contains(search_term, case=False)]
    
    if not matches.empty:
        st.success(f"Found {len(matches)} articles matching '{search_term}'")
        
        # Add Green Dots on top of the line chart
        fig.add_trace(
            go.Scatter(
                x=matches["date"],
                y=matches["pageviews"],
                mode="markers",
                marker=dict(color="#00CC96", size=15, symbol="circle-open-dot", line=dict(width=3)),
                name="Search Matches",
                text=matches["article"],
                hovertemplate="<b>MATCH: %{text}</b><br>Date: %{x|%b %d}<br>Views: %{y:,}"
            )
        )
    else:
        st.warning(f"No articles found matching '{search_term}'")

# --- 7. Final Display ---
fig.update_layout(
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="Pageviews"
)

st.plotly_chart(fig, use_container_width=True)

# Optional: Show table of matching articles
if search_term and not matches.empty:
    with st.expander("View Search Results Data", expanded=True):
        st.dataframe(matches[["date", "article", "pageviews", "Period"]])