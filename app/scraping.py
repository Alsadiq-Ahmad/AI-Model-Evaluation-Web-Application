# app/scraping.py
import requests
from bs4 import BeautifulSoup
import pinecone

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = extract_data(soup)
    store_in_vector_db(data)

def extract_data(soup):
    data = []
    for p in soup.find_all('p'):
        data.append(p.get_text())
    return data

def store_in_vector_db(data):
    pinecone.init(api_key="6b677b06-9315-4675-9d94-090f47b4ee9b")
    index = pinecone.Index('pwc')
    vectors = [(i, vec) for i, vec in enumerate(data)]
    index.upsert(vectors)
