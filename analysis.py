import pandas as pd
from textblob import TextBlob

# 1. Load data (CSV format agar file .csv hai toh)
file_path = 'data/amazon_reviews.csv' 
df = pd.read_csv(file_path)

# 2. Columns select karna (Saare 20+ columns ki zaroorat dashboard mein nahi hogi)
# Hum zaroori columns rakh rahe hain: brand, categories, name, reviews.rating, reviews.text
important_cols = ['id', 'brand', 'categories', 'name', 'reviews.rating', 'reviews.text', 'reviews.title', 'reviews.date']
df = df[important_cols]

# 3. Cleaning: Khali reviews ko hatayein
df.dropna(subset=['reviews.text'], inplace=True)

# 4. Sentiment Analysis Function
def get_sentiment(text):
    score = TextBlob(str(text)).sentiment.polarity
    if score > 0: return 'Positive'
    elif score == 0: return 'Neutral'
    else: return 'Negative'

# Apply sentiment
print("Processing Sentiment Analysis...")
df['Sentiment'] = df['reviews.text'].apply(get_sentiment)

# 5. Final Cleaned File Save karna
df.to_csv('data/cleaned_amazon_reviews.csv', index=False)
print("Done! Cleaned file 'data/cleaned_amazon_reviews.csv' ready hai.")