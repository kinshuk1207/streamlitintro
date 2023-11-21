import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import ast

# Function to load and process data
@st.cache_data
def load_and_process_data():
    data = pd.read_csv('book_word_frequencies_updated.csv')
    # Convert the 'Most Common Words' column from string to list of tuples
    data['Most Common Words'] = data['Most Common Words'].apply(ast.literal_eval)

    # Assuming the 'Title' column contains dates like "Oct 1, 1993"
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['Year'] = data['Date'].dt.year

    # Optionally handle missing or malformed data
    data = data.dropna(subset=['Year'])

    return data

def aggregate_word_frequencies_by_year(data):
    year_word_freq = {}
    for year in data['Year'].unique():
        year_data = data[data['Year'] == year]
        word_freq = Counter()
        for _, row in year_data.iterrows():
            word_freq += Counter(dict(row['Most Common Words']))
        year_word_freq[year] = word_freq
    return year_word_freq

# Main app function
def main():
    st.title("Word Frequency Analysis by Year")

    # Load and process your data
    data = load_and_process_data()

    # Aggregate word frequencies by year
    year_word_freq = aggregate_word_frequencies_by_year(data)

    # Sidebar for year selection
    st.sidebar.title("Options")
    selected_year = st.sidebar.selectbox("Select Year", sorted(data['Year'].unique()))

    # Display the most common words for the selected year
    st.header(f"Most Frequent Words in {selected_year}")
    common_words = year_word_freq[selected_year].most_common(10)
    words, counts = zip(*common_words)
    fig, ax = plt.subplots()
    ax.bar(words, counts)
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    st.dataframe(year_word_freq[selected_year])
    
    df_temp = pd.read_csv('gutenberg_top_100_with_metadata.csv')
    
    st.dataframe(df_temp)


if __name__ == "__main__":
    main()
