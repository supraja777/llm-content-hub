from crawler import load_documents, get_all_blog_links
from storage import url_store
from constants import BATCH_SIZE
from chunker import chunk_documents
from embedder import embeddings
from vectorstore import build_or_update_vector_db
from langchain_core.documents import Document

from logging_config import setup_logging
import logging

setup_logging()

# 1 Loading existing urls
existing_urls = url_store.load_stored_urls()
existing_urls_set = set(existing_urls) # for O(1) lookup time 

# 2 Crawling data to get all links
today_urls = get_all_blog_links()

# 3 Filtering new links
new_urls = [u for u in today_urls if u not in existing_urls_set]

# 4 Save urls in stored_urls.json
url_store.save_stored_urls(new_urls)

if new_urls:
    logging.info("New urls found today....")

    # 5 Loading documents in batch to avoid memory spikes
    for i in range(0, len(new_urls), BATCH_SIZE):
        batch = new_urls[i: i + BATCH_SIZE]
        try:
            docs = load_documents(new_urls)
            logging.info(f"Loaded batch {i//BATCH_SIZE + 1} of {len(new_urls)//BATCH_SIZE + 1}")
        except Exception as e:
            logging.info(f"Error loading batch {i//BATCH_SIZE + 1} : {e}")

    logging.info("Completed creating documents")

    # 6 Loading documents in batch to avoid memory spikes
    chunks = chunk_documents(docs)
    logging.info("Created chunks")

    # 7 Insert into vector DB
    build_or_update_vector_db(chunks, embeddings)
    logging.info("Inserted chunks into FAISS vector store")

else:
    logging.info("No new URLs found today!")