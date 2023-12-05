import pandas as pd

# Load the metadata CSV
metadata_df = pd.read_csv('gutenberg_top_1000_with_metadata.csv')

# Load the word frequency CSV
word_freq_df = pd.read_csv('book_word_frequencies.csv')

# Rename 'ID' column in metadata_df to 'Book ID' to match the word_freq_df
metadata_df.rename(columns={'ID': 'Book ID'}, inplace=True)

# Merge the dataframes using a left join
merged_df = pd.merge(metadata_df, word_freq_df, on='Book ID', how='left')

# Save the merged dataframe to a new CSV
merged_df.to_csv('merged_books_data.csv', index=False)
