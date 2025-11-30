import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from typing import List

from pydantic import Json

from vectorstore import load_vector_db, retrieve_documents
from embedder import embeddings
from datetime import datetime
from llm_chains.llm_chains import summarize_content_chain

from logging_config import setup_logging
import logging

setup_logging()

from constants import PATH

def retrieve_docs(path:str, query:str):
    logging.info("Retrieving documents from vector db")

    vector_db = load_vector_db(embeddings, path)
    results = retrieve_documents(query, vector_db, 7)
    retrieved_documents = [r for r in results if 
                           r.metadata["fetched_at"] ==  datetime.today().date().isoformat()]
    return retrieved_documents
    
#contentList.extend((doc.metadata["source"], summarize_content(doc.page_content)))

def generateContentList(query: str) -> List[Json]:
    # 1. User selected topi -> query

    # 2. Retrieve documents from vector store, filter by date
    retrieved_docs = retrieve_docs(path = PATH, query = query)

    # 3. Use an LLM to aggregate the information
    contentList = []
    for doc in retrieved_docs:   
        contentList.append({
            "source": doc.metadata["source"],
            "summary": summarize_content_chain(doc.page_content)
        })

    return contentList


# TODO - 
# 4 Use an LLM to check for fact checking 
# 5 Check for hallucinations
# 6 Return to user - through flash cards - Good UI!!!