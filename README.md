# Reddit-Bitcoin-Sentiment-Analyzer

# Project Overview

This project analyzes and visualizes the potential correlation between public sentiment on the r/Bitcoin subreddit and the historical price of Bitcoin. By combining data from social media and financial markets, the project aims to provide insights into how community sentiment might relate to market movements.

## Methodology

   - Reddit Data Collection: Used the PRAW library to scrape 1,000 recent posts from the r/Bitcoin subreddit.

   - Sentiment Analysis: Applied the VADER (vaderSentiment) model to calculate a sentiment score (from -1.0 to +1.0) for each post, and then computed a daily average sentiment score.

   - Price Data Retrieval: Utilized the yfinance library to fetch historical closing prices and trading volume for Bitcoin (BTC-USD).

   - Data Integration: Merged the daily sentiment scores with the historical price data into a single pandas DataFrame based on the date.

   - Visualization & Correlation: Employed matplotlib to create a dual-panel visualization showing price, volume, and sentiment trends. A correlation coefficient was calculated to quantify the relationship between sentiment and price.

## Key Findings :

   - Positive Sentiment: The analysis showed that sentiment within the r/Bitcoin community was consistently positive during the data collection period.

   - Positive Correlation: A calculated correlation coefficient of approximately 0.32 indicates a weak-to-moderate positive relationship between daily sentiment and Bitcoin's closing price.

## Limitations

   - The project used a limited dataset of approximately 14 days, so the findings may not represent long-term trends.

   - Correlation does not imply causation. Further analysis is needed to understand the underlying dynamics.

## How to Run the Project

   - Clone the repository.

   - Set up a virtual environment and install the required libraries: pip install -r requirements.txt.

   - Create a Reddit Developer Account and generate your client_id and client_secret.

   - Create a .env file in the same directory as the script and add your API keys:

      REDDIT_CLIENT_ID="your_client_id_here"
      REDDIT_CLIENT_SECRET="your_client_secret_here"

   - Run the script: python Real_Project.py
