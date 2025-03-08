import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import time
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

# Function to fetch data from Google Sheets
@st.cache_data(ttl=60)  # Cache for 60 seconds to avoid frequent requests
def get_google_sheet_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1NsxHZpkMTPczAGh0yCrrAoE-rlmpSKfbuL8gTblBeRg/gviz/tq?tqx=out:csv&gid=0"
    return pd.read_csv(sheet_url)

# Function to extract keywords using TF-IDF
def extract_keywords(text_data, top_n=20):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)
    X = vectorizer.fit_transform([text_data])
    keywords = vectorizer.get_feature_names_out()
    return " ".join(keywords)

# Streamlit UI
st.title("Live Word Cloud from Survey Responses")

while True:
    try:
        df = get_google_sheet_data()
        if not df.empty:
            text_data = " ".join(df[df.columns[-1]].dropna())  # Assuming last column has responses
            filtered_text = extract_keywords(text_data)  # Extract only relevant keywords
            
            # Clear previous word cloud
            st.empty()
            
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
        
        time.sleep(10)  # Refresh every 10 seconds
    except Exception as e:
        st.error(f"Error fetching data: {e}")
