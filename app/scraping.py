import requests
from bs4 import BeautifulSoup
import re
from pinecone import Pinecone, ServerlessSpec
from urllib.parse import urljoin

# Initialize Pinecone
pc = Pinecone(
    api_key="" #pincone api
)

# Create index if it doesn't exist
if 'pwc' not in pc.list_indexes().names():
    pc.create_index(
        name='pwc',
        dimension=512,
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-west-2'
        )
    )
index = pc.Index('pwc')

# Function to scrape a single URL
def scrape_website(url, visited=set()):
    if url in visited:
        return []
    
    visited.add(url)
    print(f"Scraping {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []
    
    content_type = response.headers.get('Content-Type', '')
    
    if 'text/html' in content_type:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            data = extract_data(soup)
            store_in_vector_db(data)  # Store data after scraping each URL
            subpages = find_subpages(soup, url)
            for subpage in subpages:
                scrape_website(subpage, visited)
        except Exception as e:
            print(f"Failed to parse HTML: {e}")
            data = []
    else:
        print(f"Unsupported content type: {content_type}")
        data = []
    
    return data

# Function to extract textual data from the BeautifulSoup object
def extract_data(soup):
    paragraphs = soup.find_all('p')
    return [p.get_text() for p in paragraphs]

# Function to find subpage links
def find_subpages(soup, base_url):
    links = soup.find_all('a', href=True)
    subpages = []
    base_domain = re.match(r"https?://[^/]+", base_url).group(0)
    
    for link in links:
        href = link['href']
        if href.startswith('/'):
            subpages.append(urljoin(base_domain, href))
        elif href.startswith(base_domain):
            subpages.append(href)
    
    return subpages

# Function to store data in Pinecone vector database
def store_in_vector_db(data):
    vectors = []
    for i, text in enumerate(data):
        # Ensure the vector is of dimension 512
        vector = [float(ord(c)) for c in text[:512]]
        vector += [0.0] * (512 - len(vector))  # Padding with zeros if needed
        vectors.append((str(i), vector))
    index.upsert(vectors)

# Main script
if __name__ == "__main__":
    main_url = "https://u.ae/en/information-and-services"

    # Scrape the main URL and its subpages
    scrape_website(main_url)
    print(f"Data from {main_url} and its subpages stored in Pinecone.")
