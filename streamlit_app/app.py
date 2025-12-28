

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")

# Streamlit Page Settings
st.set_page_config(page_title="Airbnb London Dashboard", layout="wide")
st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }
    h1, h2, h3 {
        color: #1f2c56;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#Adding background color in the sidebar
st.markdown(
    """
    <style>
    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #eef2f7;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label {
        color: #1f2c56;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Load & Prepare Data 
df=pd.read_csv("data/listings_clean_2.csv")


# clean price column
df["price"] = df["price"].replace('[\$,]', '', regex=True).astype(float)

#    Title 
st.title("🏙️ Airbnb London Analytics Dashboard")
st.markdown("""
This interactive dashboard allows you to explore **pricing**, **availability**, and **host behaviour** 
for Airbnb listings in **London**.  
Use the filters on the left to customize the view.
""")

# SIDEBAR FILTERS 
st.sidebar.header("🔍 Filters")

# 1. Neighbourhood Filter  (CHANGED)
neighs = sorted(df["neighbourhood_cleansed"].dropna().unique())
selected_neigh = st.sidebar.selectbox("Select Neighbourhood", ["All"] + neighs)

# 2. Room Type Filter
room_types = df["room_type"].unique()
selected_room = st.sidebar.multiselect("Select Room Type(s)", room_types, default=room_types)

# 3. Price Range Slider
min_p = int(df["price"].min())
max_p = int(df["price"].max())
selected_price = st.sidebar.slider("Select Price Range (£)", min_p, max_p, (min_p, max_p))

#    APPLY FILTERS  
df_filtered = df.copy()

if selected_neigh != "All":
    df_filtered = df_filtered[df_filtered["neighbourhood_cleansed"] == selected_neigh]

df_filtered = df_filtered[df_filtered["room_type"].isin(selected_room)]
df_filtered = df_filtered[(df_filtered["price"] >= selected_price[0]) & (df_filtered["price"] <= selected_price[1])]

# KPI CARDS 
st.subheader("📌 Key Metrics")

k1, k2, k3 = st.columns(3)

k1.metric(
    label="🏘️ Total Listings",
    value=f"{len(df_filtered):,}"
)

k2.metric(
    label="💷 Average Price",
    value=f"£{df_filtered['price'].mean():.0f}"
)

k3.metric(
    label="⭐ Avg Review Score",
    value=f"{df_filtered['review_scores_rating'].mean():.1f}"
)


# Plot1: Price Distribution
st.subheader("📊 Price Distribution")

fig1, ax1 = plt.subplots(figsize=(7, 4))
sns.histplot(
    df_filtered["price"],
    bins=50,
    kde=True,
    color="#4c72b0",
    ax=ax1
)
ax1.set_xlabel("Price (£)")
ax1.set_xlim(0, 1000)
ax1.grid(alpha=0.3)

st.pyplot(fig1)


# Plot2: Avg Price by Room Type
st.subheader("🏠 Average Price by Room Type")

fig2, ax2 = plt.subplots(figsize=(7, 4))
sns.barplot(
    data=df_filtered,
    x="room_type",
    y="price",
    palette="Set2",
    ax=ax2
)
ax2.set_ylabel("Average Price (£)")
ax2.grid(axis="y", alpha=0.3)

st.pyplot(fig2)


# TOP NEIGHBOURHOODS 
top_neigh = (
    df_filtered.groupby("neighbourhood_cleansed")["price"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# Plot 3: Avg Price by Neighbourhood
st.subheader("📍 Top 10 Neighbourhoods by Average Price")

fig3, ax3 = plt.subplots(figsize=(7, 5))
sns.barplot(
    data=top_neigh,
    x="price",
    y="neighbourhood_cleansed",
    palette="Blues_r",
    ax=ax3
)
ax3.set_xlabel("Average Price (£)")
ax3.grid(axis="x", alpha=0.3)

st.pyplot(fig3)


#Plot 4: Number of listings by room type
st.subheader("📦 Number of Listings by Room Type")

room_counts = df_filtered["room_type"].value_counts().reset_index()
room_counts.columns = ["room_type", "count"]

fig4, ax4 = plt.subplots(figsize=(7, 4))
sns.barplot(
    data=room_counts,
    x="room_type",
    y="count",
    palette="Set3",
    ax=ax4
)
ax4.set_ylabel("Number of Listings")
ax4.grid(axis="y", alpha=0.3)

st.pyplot(fig4)

#PLOT 5: Reviews vs Price
st.subheader("💬 Price vs Number of Reviews")

fig5, ax5 = plt.subplots(figsize=(7, 4))
sns.scatterplot(
    data=df_filtered,
    x="price",
    y="number_of_reviews",
    alpha=0.4,
    ax=ax5
)
ax5.set_xlim(0, 1000)
ax5.set_xlabel("Price (£)")
ax5.set_ylabel("Number of Reviews")
ax5.grid(alpha=0.3)

st.pyplot(fig5)

#PLOT 6: Review score distribution
st.subheader("⭐ Review Score Distribution")

fig6, ax6 = plt.subplots(figsize=(7, 4))
sns.histplot(
    df_filtered["review_scores_rating"].dropna(),
    bins=20,
    kde=True,
    color="#dd8452",
    ax=ax6
)
ax6.set_xlabel("Review Score")
ax6.grid(alpha=0.3)

st.pyplot(fig6)



# TABLE 
st.subheader("📄 Filtered Listings (Top 30 by Price)")

table_df = (
    df_filtered[
        ["name", "neighbourhood_cleansed", "room_type", "price", "number_of_reviews"]
    ]
    .sort_values("price", ascending=False)
    .head(30)
)
styled_df = table_df.style.background_gradient(
    subset=["price"],
    cmap="Reds"
)

st.dataframe(
    styled_df,
    use_container_width=True,
    height=420
)


