import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm

def get_book_metadata(book_id):
    """Fetch metadata for a specific book from its Gutenberg page."""
    book_url = f"https://www.gutenberg.org/ebooks/{book_id}"
    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting the author
    author_row = soup.find('th', string='Author')
    author_name = author_row.find_next_sibling('td').get_text(strip=True) if author_row else 'Unknown'


    # Extracting the publication date
    pub_date_row = soup.find('tr', property="dcterms:issued")
    publication_date = pub_date_row.find('td').get_text(strip=True) if pub_date_row else 'Unknown'

    # Extracting the language
    language_row = soup.find('tr', property="dcterms:language")
    book_language = language_row.find('td').get_text(strip=True) if language_row else 'Unknown'

    # Extracting LoC Class
    loc_class_row = soup.find('tr', property="dcterms:subject", datatype="dcterms:LCC")
    loc_class = loc_class_row.find('td').get_text(strip=True) if loc_class_row else 'Unknown'

    # Extracting subjects
    subjects = []
    subject_rows = soup.find_all('tr')
    for row in subject_rows:
        if row.find('th') and row.find('th').get_text(strip=True) == 'Subject':
            subject = row.find('td').get_text(strip=True)
            subjects.append(subject)

    return {
        'author': author_name,
        'publication_date': publication_date,
        'language': book_language,
        'loc_class': loc_class,
        'subjects': subjects
    }


# URL for Project Gutenberg's Top 1000 eBooks for the last 30 days
url = "https://www.gutenberg.org/browse/scores/top1000.php"

# Send a request to the URL
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the list of top 100 books
book_list = soup.find_all('ol')[0]
books = book_list.find_all('li')

# Collect metadata for each book
top_books = []
for book in tqdm(books):
    title = book.get_text()
    link = book.find('a')['href']
    book_id = link.split('/')[-1]
    
    # Fetch additional metadata
    metadata = get_book_metadata(book_id)
    top_books.append([
        book_id, title, metadata['author'], metadata['publication_date'], 
        metadata['language'], metadata['loc_class'], ', '.join(metadata['subjects']), 
        f"https://www.gutenberg.org{link}"
    ])
    

# Specify the path for the CSV file
csv_filename = './gutenberg_top_1000_with_metadata.csv'

# Write data to CSV
with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['ID', 'Title', 'Author', 'Publication Date', 'Language', 'LoC Class', 'Subjects', 'Link'])
    writer.writerows(top_books)

print(f"CSV file created at {csv_filename}")
