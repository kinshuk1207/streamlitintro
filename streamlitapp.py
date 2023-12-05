import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import ast
import random
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# Load and process data
@st.cache_data()

def parse_subjects(subject_str):
    # Split the string by comma and strip whitespace
    return [subj.strip() for subj in subject_str.split(',')]


def load_and_process_data():
    data = pd.read_csv('merged_books_data.csv')
    
    # Replace NaN in 'Most Common Words' with an empty list
    data['Most Common Words'] = data['Most Common Words'].fillna("[]")

    # Convert the 'Most Common Words' column from string to list of tuples
    data['Most Common Words'] = data['Most Common Words'].apply(ast.literal_eval)

    data['Publication Date'] = pd.to_datetime(data['Publication Date'], errors='coerce')
    data['Year'] = data['Publication Date'].dt.year
    
    # Apply the custom parser to the 'Subjects' column
    data['Subjects'] = data['Subjects'].fillna("").apply(parse_subjects)


    return data


# Aggregate word frequencies by year
def aggregate_word_frequencies(data, column):
    yearly_data = {}
    for year in sorted(data['Year'].unique()):
        words = Counter()
        year_rows = data[data['Year'] == year]
        for row in year_rows[column]:
            words.update(Counter(dict(row)))
        yearly_data[year] = words
    return yearly_data

def subject_similarity(book1, book2):
    # Convert subjects to sets and calculate Jaccard similarity
    subjects1 = set(book1)
    subjects2 = set(book2)
    intersection = subjects1.intersection(subjects2)
    union = subjects1.union(subjects2)
    if not union:
        return 0
    return len(intersection) / len(union)

def word_frequency_similarity(book1, book2):
    # Flatten word-frequency tuples into a single string
    words1 = " ".join([word for word, count in book1 for _ in range(count)])
    words2 = " ".join([word for word, count in book2 for _ in range(count)])

    # Check if either word list is empty
    if not words1 or not words2:
        return 0

    # Vectorize the word frequency strings
    try:
        vectorizer = CountVectorizer().fit([words1, words2])
        vectors = vectorizer.transform([words1, words2]).toarray()
        return cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    except ValueError:
        # Handle the case where CountVectorizer fails (e.g., due to empty vocabulary)
        return 0


def find_similar_books(selected_book, data, top_n=5):
    similarities = []
    for _, book in data.iterrows():
        if book['Book ID'] == selected_book['Book ID']:
            continue
        subj_sim = subject_similarity(selected_book['Subjects'], book['Subjects'])
        word_freq_sim = word_frequency_similarity(selected_book['Most Common Words'], book['Most Common Words'])
        avg_sim = (subj_sim + word_freq_sim) / 2
        similarities.append((book['Title_x'], avg_sim))

    # Sort by average similarity and return the top N
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]


def random_book_suggestion(data):
    st.title("Random Book Suggestion")
    random_book = data.sample(1).iloc[0]
    st.write("Random Book Metadata:")
    st.dataframe(random_book[['Title_x', 'Author', 'Publication Date', 'Link']])
    
    # Format and display the most common words
    st.write("Most Common Words:")
    most_common_words = random_book['Most Common Words']
    formatted_words = ', '.join([f"{word} ({count})" for word, count in most_common_words])
    st.write(formatted_words)

    # Find and display similar books
    similar_books = find_similar_books(random_book, data)
    st.write("Books Similar to Selected Book:")
    for title, sim_score in similar_books:
        st.write(f"{title} (Similarity Score: {sim_score:.2f})")

def search_results(data, query):
    # Filter data for the book title matching the search query
    result = data[data['Title_x'].str.contains(query, case=False, na=False)]

    if not result.empty:
        # Assuming the first match is the desired one
        book = result.iloc[0]
        st.write("Book Metadata:")
        st.dataframe(book[['Title_x', 'Author', 'Publication Date', 'Link']])
        
        # Display the most common words
        st.write("Most Common Words:")
        most_common_words = book['Most Common Words']
        formatted_words = ', '.join([f"{word} ({count})" for word, count in most_common_words])
        st.write(formatted_words)

        # Find and display similar books
        similar_books = find_similar_books(book, data)
        st.write("Books Similar to Selected Book:")
        for title, sim_score in similar_books:
            st.write(f"{title} (Similarity Score: {sim_score:.2f})")
    else:
        st.write("No matching books found.")

# Main application
def main():
    data = load_and_process_data()

    st.title("Book Analysis Dashboard")
    
    # Search functionality
    search_query = st.text_input("Search for a book title")

    if search_query:
        search_results(data, search_query)

    page = st.sidebar.selectbox("Choose a function", ["Home", "Trend Analysis", "Random Book Suggestion"])

    if page == "Home":
        st.write("Welcome to the Book Analysis Dashboard!")
    elif page == "Trend Analysis":
        trend_analysis(data)
    elif page == "Random Book Suggestion":
        random_book_suggestion(data)


def aggregate_subjects(data):
    subjects_by_year = {}
    for year in sorted(data['Year'].unique()):
        subjects = Counter()
        for subj_list in data[data['Year'] == year]['Subjects']:
            subjects.update(subj_list)
        subjects_by_year[year] = subjects
    return subjects_by_year

def subject_trends(data):
    st.title("Subject Trends Over Time")
    subject_data = aggregate_subjects(data)
    year = st.selectbox("Select Year", sorted(subject_data.keys()))
    show_top_subjects(subject_data, year)

def show_top_subjects(subject_data, year):
    st.write(f"Top subjects for the year {year}")
    common_subjects = subject_data[year].most_common(10)
    subjects, counts = zip(*common_subjects)
    fig, ax = plt.subplots()
    ax.bar(subjects, counts)
    plt.xticks(rotation=45)
    ax.set_xlabel('Subjects')  # Label for the x-axis
    ax.set_ylabel('Count')  # Label for the y-axis
    ax.set_title(f"Subject Trends in {year}")  # Adding a title for clarity
    st.pyplot(fig)


# Trend Analysis
def trend_analysis(data):
    st.title("Trend Analysis")
    analysis_type = st.radio("Select analysis type", ["Word Frequency Trends", "Subject Trends"])

    if analysis_type == "Word Frequency Trends":
        word_freq_data = aggregate_word_frequencies(data, 'Most Common Words')
        year = st.selectbox("Select Year", sorted(word_freq_data.keys()))
        show_top_words(word_freq_data, year)
    elif analysis_type == "Subject Trends":
        subject_trends(data)

# Display top words for the selected year
def show_top_words(word_freq_data, year):
    st.write(f"Top words for the year {year}")
    common_words = word_freq_data[year].most_common(10)

    if common_words:
        words, counts = zip(*common_words)
        fig, ax = plt.subplots()
        ax.bar(words, counts)
        plt.xticks(rotation=45)
        ax.set_xlabel('Words')
        ax.set_ylabel('Frequency')
        ax.set_title(f"Word Frequency in {year}")
        st.pyplot(fig)
    else:
        st.write("No word frequency data available for this year.")


if __name__ == "__main__":
    main()
