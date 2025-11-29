from langchain_community.document_loaders import WebBaseLoader
from typing import List
from bs4 import BeautifulSoup
from constants import BASE_URL
import requests
from datetime import datetime

def load_documents(urls: List[str]):
    print("Loading documents")
    docs = []
    for url in urls:
        loaded = WebBaseLoader(url).load()
        for doc in loaded:
            if doc.metadata is None:
                doc.metadata = {}
            doc.metadata["fetched_at"] = datetime.today().date().isoformat()
        docs.extend(loaded)
    return docs

def get_all_blog_links():
    print("Crawling")
    url = f"{BASE_URL}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]

        if href.startswith("/articles/") and href != "/articles":
            full_url = BASE_URL + href
            links.append(full_url)

    return list(dict.fromkeys(links))