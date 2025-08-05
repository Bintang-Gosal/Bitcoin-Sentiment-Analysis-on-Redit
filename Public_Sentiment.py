import os
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import praw

system_os = os.name

match system_os:
    case "posix": os.system("clear")
    case "nt": os.system("cls")

load_dotenv()

# Replace with your own API
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = "crypto_sentiment_project"

# Authentication with Reddit API
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Gather post about Bitcoin on Subredit 
subreddit = reddit.subreddit("Bitcoin")
posts = subreddit.new(limit=1000) # replace 'hot' with 'new' if u want the newest post

posts_data = []
for post in posts:
    posts_data.append({
        "Date": pd.to_datetime(post.created_utc, unit='s'),
        "Post_Title": post.title,
        'Text_Post': post.selftext
    })

# make the DataFrame
df_reddit = pd.DataFrame(posts_data)

# show the first 5 row
print(df_reddit.head())

# gather the title and the text post for more comprehensive analysis
df_reddit["Full_Text"] = df_reddit["Post_Title"] + ' ' + df_reddit["Text_Post"]

# vader initialiation
analyzer = SentimentIntensityAnalyzer()

# function for sentiment scor compund
def get_sentiment_score(text):
    if not isinstance(text, str) or text.strip() == "":
        return 0
    vs = analyzer.polarity_scores(text)
    return vs["compound"]

df_reddit["sentiment_score"] = df_reddit["Full_Text"].apply(get_sentiment_score)

df_reddit["Date"] = df_reddit["Date"].dt.date

# count the average sentiment per day
day_sentiment = df_reddit.groupby("Date")["sentiment_score"].mean().reset_index()

# show the first 5 round form day sentiment
print(f"Average sentiment per-Day :\n{day_sentiment}\n")

# take the historic price bitcoin for the sam period with the sentiment data
price_data = yf.download("BTC-USD", period="3mo", interval="1d")

# flatten the multi level columb index from y finance
price_data.columns = price_data.columns.get_level_values(0)

# make sure the date index on dataframe fit to merge
price_data.index = price_data.index.date 

day_sentiment.rename(columns={"Date": "Date"}, inplace=True)
day_sentiment.set_index("Date", inplace=True)

# merge data sentiment with price data
final_data = pd.merge(price_data, day_sentiment, left_index=True, right_index=True)

# check the DataFrame
print(f"DataFrame after merging (5 first row): \n{final_data.head()}\n")

real_corelation = final_data['sentiment_score'].corr(final_data['Close'])
print(f"Coefficient Sentiment Reddit and Price:\n{real_corelation}\n")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True)

ax1.set_title('Bitcoin Price and Volume', fontsize=16)
ax1.set_ylabel('Price (USD)', color='black', fontsize=12)
ax1.plot(final_data.index, final_data['Close'], color='black', label='Closing Price')
ax1.tick_params(axis='y', labelcolor='black')

ax1_twin = ax1.twinx()
ax1_twin.set_ylabel('Volume', color='grey', fontsize=12)
ax1_twin.bar(final_data.index, final_data['Volume'], color='grey', alpha=0.3)
ax1_twin.tick_params(axis='y', labelcolor='grey')

# ----------------------------------------

ax2.set_title('Average Public Sentiment (14 day) From Reddit', fontsize=16)
ax2.set_xlabel('Date', fontsize=12)
ax2.set_ylabel('Sentiment Score', color='black', fontsize=12)
ax2.plot(final_data.index, final_data['sentiment_score'], color='red')
ax2.tick_params(axis='y', labelcolor='red')

ax2.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)

fig.tight_layout(pad=3.0)

plt.show()