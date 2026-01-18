
# Ankita Ankita
# London Airbnb Analysis Dashboard

Airbnb London Analytics Dashboard

This project analyzes Airbnb listings in London and presents the results through an interactive Streamlit dashboard. The dashboard allows users to explore patterns in pricing, availability, and listing characteristics using filters for neighbourhood, room type, and price range.

## Running the Dashboard

To run the Streamlit dashboard locally:
1. Download the dataset from Kaggle (link above)
2. Run the preprocessing notebook to generate `listings_clean_2.csv`
3. Place the cleaned file in the "data" directory
4. Run:
   streamlit run streamlit_app/app.py


# Dataset

The dataset used in this project was sourced from Kaggle:
https://www.kaggle.com/datasets/sukanto/airbnb-london-listings-data

# Data Preprocessing

The initial data preprocessing was performed in a Jupyter Notebook, where the raw Airbnb listings data was cleaned and prepared for analysis. This process included handling missing values, formatting variables, and selecting relevant features. After preprocessing, the cleaned dataset was saved as listings_clean_2.csv.

The cleaned file was then used as the input for the Streamlit application. It was loaded by the app.py script located in the streamlit_app folder. The dashboard was launched by running the Streamlit application from the terminal, which opens an interactive web interface for exploration.

# Dashboard Features

The dashboard enables users to:

Filter listings by neighbourhood, room type, and price range

View key summary metrics such as total number of listings, average price, and average review score

Several visualizations are included to support deeper analysis. These include a price distribution plot to examine the spread and skewness of listing prices, as well as additional charts showing how prices and availability vary across neighbourhoods and room types. These visualizations help identify trends, outliers, and differences within the London Airbnb market.

# Conclusion

Overall, this project demonstrates how interactive data visualization can be used to gain insights from large real-world datasets and communicate results in an intuitive and user-friendly way.

