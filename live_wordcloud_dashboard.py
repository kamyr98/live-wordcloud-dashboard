import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import random
import time

# Function to fetch data from Google Sheets
@st.cache_data(ttl=60)  # Cache for 60 seconds to avoid frequent requests
def get_google_sheet_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1NsxHZpkMTPczAGh0yCrrAoE-rlmpSKfbuL8gTblBeRg/gviz/tq?tqx=out:csv&gid=0"
    return pd.read_csv(sheet_url)

# Function to generate a word cloud with different colors for each response
def generate_colored_wordcloud(responses):
    color_choices = ["red", "blue", "green", "purple", "orange", "pink", "brown", "gray"]
    word_frequencies = {response: random.randint(1, 10) for response in responses}  # Random sizes for visualization
    
    def color_func(word, **kwargs):
        return random.choice(color_choices)  # Assign random colors to responses
    
    wordcloud = WordCloud(width=1200, height=600, background_color='white', 
                          colormap=None, color_func=color_func, collocations=False,
                          prefer_horizontal=0.5, max_words=len(responses),
                          min_font_size=10, max_font_size=200)
    wordcloud.generate_from_frequencies(word_frequencies)
    return wordcloud

# Streamlit UI
st.title("Live Word Cloud from Survey Responses")

placeholder = st.empty()  # Placeholder for dynamic content

while True:
    try:
        df = get_google_sheet_data()
        if not df.empty:
            responses = df[df.columns[-1]].dropna().tolist()  # Collect all responses
            
            # Generate Word Cloud with varied colors, random positioning, and vertical words
            wordcloud = generate_colored_wordcloud(responses)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            
            # Update the placeholder with the new word cloud
            with placeholder.container():
                st.pyplot(fig)
        else:
            placeholder.write("Waiting for responses...")
        
        time.sleep(10)  # Refresh every 10 seconds
    except Exception as e:
        placeholder.error(f"Error fetching data: {e}")
