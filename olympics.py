import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Popular topics during and after Olympics 2024") 
st.markdown("---")

    # --- Introduction Section ---
st.header("1. Introduction and Project Goal")
st.markdown("""
        **Data Description:** This dataset contains **popular topics based on public interests during 2024 summer Olympics from July 26, 2024 to August 11, 2024 for all countries and the article topics of a month later.**

        **Questions:** 
        - Is there any differences between popular articles topics during **2024 summer Olympics** and **a month later**?
        - What are the top 10 languages from the top 100 articles based on public interests during Olympics and one month later?
        - What are the differences between sports/nonsports articles during Olympics and a month later?
        
        **Interaction:** Use the interactive widgets to poke around to see different insights from data.
    """)
st.markdown("---")

df_o = pd.read_csv("data/sort_100.csv")
df_a = pd.read_csv("data/sort_100_after.csv")
df_all = pd.read_csv("data/alldata.csv")

st.write("First, We are exploring the top 100 articles during 2024 summer Olympics and then we explore data for one month later")


page = st.sidebar.radio("Select Page", ["Top 100 Articles", "Sports vs Non-Sports", "Languages"])

df_all['date'] = pd.to_datetime(df_all['date'])

if page == "Top 100 Articles":
    st.title("Top 100 Articles During Olympics & One Month Later")

    # Country dropdown
    country_list = ["All"] + sorted(df_o["country_code"].unique())
    selected_country = st.selectbox("Country", country_list)

    # Date range slider (on main page)
    min_date = df_all['date'].min().to_pydatetime()
    max_date = df_all['date'].max().to_pydatetime()
    date_range = st.slider(
        "Select date range for analysis",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )

    # Filter Top 100 by country
    df_filtered = df_o.copy()
    if selected_country != "All":
        df_filtered = df_filtered[df_filtered['country_code'] == selected_country]

    # -------------------------
    # 1️⃣ Top 100 Table (During Olympics)
    # -------------------------
    st.subheader("Top 100 Articles Table (During Olympics)")
    df_filtered_sorted = df_filtered.sort_values("total_pageviews", ascending=False)
    st.dataframe(df_filtered_sorted)

    # -------------------------
    # 2️⃣ Top 20 Articles Bar Chart (During Olympics)
    # -------------------------
    st.subheader("Top 20 Articles by Pageviews (During Olympics)")
    top20 = df_filtered_sorted.head(20)
    st.bar_chart(top20.set_index("article")["total_pageviews"])

    # -------------------------
    # 3️⃣ Post-Olympics Comparison (1 Month Later)
    # -------------------------
    st.subheader("Pageviews One Month After Olympics")

    # Top 20 post-Olympics
    top20_post = df_a.head(20)
    st.bar_chart(top20_post.set_index("article")["total_pageviews"])

    # Side-by-side comparison table
    df_compare = df_filtered_sorted[['article', 'total_pageviews']].rename(columns={"total_pageviews": "Olympics"}).merge(
    df_a.rename(columns={"total_pageviews": "Post_Olympics"}), on="article", how="left").fillna(0)

    st.subheader("Olympics vs Post-Olympics Pageviews (Top 100)")
    st.dataframe(df_compare)


# -------------------------
# PAGE 2 — Sports vs Non-Sports
# -------------------------
#elif page == "Sports vs Non-Sports":
#    st.title("Sports vs Non-Sports Comparison")

    # Period selection
#    period = st.radio("Select Period", ["During Olympics", "Post Olympics", "Both"])

#    df_sport = df_filtered[df_filtered["sports"] == 1]
#    df_non = df_filtered[df_filtered["sports"] == 0]

    # Bar chart differences
 #   st.subheader("Pageviews During vs Post Olympics")
  #  sport_sum = df_sport.groupby("period")["pageviews"].sum()
   # non_sum = df_non.groupby("period")["pageviews"].sum()
    #st.bar_chart(pd.DataFrame({"Sports": sport_sum, "Non-Sports": non_sum}))

# -------------------------
# PAGE 3 — Languages
# -------------------------
#elif page == "Languages":
#    st.title("Top Languages in Top 100 Articles")
#    st.subheader("Top 10 Languages by Pageviews")
#    st.bar_chart(df_o.groupby("language")["pageviews"].sum().nlargest(10))