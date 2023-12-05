Link to the web app: https://appintro-r5r7pfpvqsttqsnd9cwxvt.streamlit.app/

Project Title: Book Trends Analysis and Recommender using Project Gutenberg 

Abstract: 
This project aims to explore literary trends using data from Project Gutenberg. The main outcome is a web application that allows users to analyze word frequency trends over time, explore subject trends, and receive book recommendations based on textual analysis.

Data Description: 
The data was sourced from Project Gutenberg's Top 1000 eBooks. It includes metadata such as title, author, publication date, language, and subjects. Additionally, word frequency data for each book was extracted and analyzed. This comprehensive dataset forms the backbone of our analysis and visualization in the web application.

Algorithm Description

Trend Analysis: Implements algorithms to analyze word frequencies and subject trends across different years. It aggregates data by year and visualizes the most common words and subjects.

Book Recommendation: Uses similarity measures to suggest books. The algorithm compares subjects and word frequencies of books to find the closest matches.

Word Frequency Extraction: Processes each book to extract and count word frequencies, removing common stopwords for a more meaningful analysis.

Tools Used

Python: The primary programming language for data processing and analysis.

Streamlit: An open-source app framework for creating interactive, data-driven web applications in Python.

Pandas: Used for data manipulation and analysis, essential for processing the dataset.

NLTK: Employed for natural language processing, particularly for stopwords removal in the word frequency analysis.

Requests and Beautiful Soup: For web scraping to extract book metadata from Project Gutenberg.

Jupyter Notebook: For initial data exploration and analysis.

Scikit-learn: For implementing cosine similarity in the recommendation algorithm.

