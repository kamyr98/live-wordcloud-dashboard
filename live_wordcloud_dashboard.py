import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import time

# Function to fetch data from Google Sheets
@st.cache_data(ttl=60)  # Cache for 60 seconds to avoid frequent requests
def get_google_sheet_data(sheet_url):
    csv_url = sheet_url.replace("/edit#gid=", "/gviz/tq?tqx=out:csv&gid=")
    return pd.read_csv(csv_url)

# Streamlit UI
st.title("Live Word Cloud from Survey Responses")

sheet_url = st.text_input("Enter Google Sheet CSV URL:")

if sheet_url:
    while True:
        try:
            df = get_google_sheet_data(sheet_url)
            if not df.empty:
                text_data = " ".join(df[df.columns[-1]].dropna())  # Assuming last column has responses
                
                # Generate Word Cloud
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                st.pyplot(plt)
            else:
                st.write("Waiting for responses...")
            
            time.sleep(10)  # Refresh every 10 seconds
        except Exception as e:
            st.error(f"Error fetching data: {e}")
