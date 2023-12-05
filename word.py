import pandas as pd
import requests
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
import csv
import time

# Ensure you have the stopwords package downloaded
nltk.download('stopwords')

def get_book_text(book_id):
    """Fetch the text of a book given its book ID."""
    url = f'https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

def preprocess_text(text):
    """Preprocess the text by removing punctuation and making it lowercase."""
    text = re.sub(r'[^\w\s]', '', text).lower()
    return text

def word_frequency_analysis(text):
    """Perform a word frequency analysis on the text."""
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords.words('english')]
    return Counter(filtered_words)

# Read the CSV file
df = pd.read_csv('gutenberg_top_1000_with_metadata.csv')

# Prepare a new CSV file to store the results
with open('book_word_frequencies.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Book ID', 'Title', 'Date', 'Most Common Words'])

    for index, row in df.iterrows():
        book_id = row['ID']  # Replace 'Book ID' with the actual column name

        print(f"Processing {row['Title']}...")
        book_text = get_book_text(book_id)
        if book_text:
            processed_text = preprocess_text(book_text)
            word_counts = word_frequency_analysis(processed_text)

            # Write the top 10 most common words for each book
            writer.writerow([book_id, row['Title'] , row['Publication Date'], word_counts.most_common(30)])

            # To prevent hitting rate limits
            time.sleep(1)
            
        

print("Word frequency analysis completed for all books.")
