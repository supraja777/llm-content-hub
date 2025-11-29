import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from vectorstore import load_vector_db, retrieve_documents
from embedder import embeddings
from datetime import datetime
from llm_chains.llm_chains import summarize_content

from logging_config import setup_logging
import logging

setup_logging()

from constants import PATH

def retrieve_docs(path:str, query:str):
    logging.info("Retrieving documents from vector db")

    vector_db = load_vector_db(embeddings, path = PATH)
    results = retrieve_documents(query, vector_db, 7)
    retrieved_documents = [r for r in results if r.metadata["fetched_at"] ==  datetime.today().date().isoformat()]
    return retrieved_documents

# 1. User will select a topic
query = "Latest updates on Large Language Models"

# 2. Retrieve documents from vector store, filter by date
retrieved_docs = retrieve_docs(path = PATH, query = query)

# 3. Use an LLM to aggregate the information
contentList = []
for doc in retrieved_docs:   
    contentList.extend((doc.metadata["source"], summarize_content(doc.page_content)))

# TODO - 
# 4 Use an LLM to check for fact checking 
# 5 Check for hallucinations
# 6 Return to user - through flash cards - Good UI!!!