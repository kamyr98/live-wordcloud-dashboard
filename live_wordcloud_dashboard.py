import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import time

# Function to fetch data from Google Sheets
@st.cache_data(ttl=60)  # Cache for 60 seconds to avoid frequent requests
def get_google_sheet_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1NsxHZpkMTPczAGh0yCrrAoE-rlmpSKfbuL8gTblBeRg/gviz/tq?tqx=out:csv&gid=0"
    return pd.read_csv(sheet_url)

# Function to extract keywords using TF-IDF
def extract_keywords(text_data, top_n=20):
    if not text_data.strip():  # Check if text is empty
        return ""
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)
    X = vectorizer.fit_transform([text_data])
    keywords = vectorizer.get_feature_names_out()
    return " ".join(keywords)

# Streamlit UI
st.title("Live Word Cloud from Survey Responses")

# Fetch Data
df = get_google_sheet_data()
if not df.empty:
    text_data = " ".join(df[df.columns[-1]].dropna())  # Assuming last column has responses
    filtered_text = extract_keywords(text_data)  # Extract only relevant keywords
    
    if filtered_text:
        # Generate Word Cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(filtered_text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.write("No relevant keywords detected in responses yet.")
else:
    st.write("Waiting for responses...")

# Auto-refresh every 10 seconds
st.experimental_rerun()
time.sleep(10)
