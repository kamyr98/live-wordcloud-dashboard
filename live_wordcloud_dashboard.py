import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import time

# Function to fetch data from Google Sheets
@st.cache_data(ttl=60)  # Cache for 60 seconds to avoid frequent requests
def get_google_sheet_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1NsxHZpkMTPczAGh0yCrrAoE-rlmpSKfbuL8gTblBeRg/gviz/tq?tqx=out:csv&gid=0"
    return pd.read_csv(sheet_url)

# Streamlit UI
st.title("Live Word Cloud from Survey Responses")

placeholder = st.empty()  # Placeholder for dynamic content

while True:
    try:
        df = get_google_sheet_data()
        if not df.empty:
            text_data_list = df[df.columns[-1]].dropna().tolist()  # Get list of responses
            combined_text = " ".join(text_data_list)  # Join responses into a single string
            
            # Generate Word Cloud with phrases preserved
            wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(combined_text)
            fig, ax = plt.subplots(figsize=(10, 5))
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
