from typing import List
from logging_config import setup_logging
import logging

setup_logging()

from langchain_community.vectorstores import FAISS
from vectorstore import load_vector_db, retrieve_documents
from constants import PATH
from embedder import embeddings
from llm_chains.llm_chains import retrieval_evaluator_chain
from websearch import knowledge_refinment, perform_web_search
from llm_chains.llm_chains import generate_response_chain

def retrieve_docs(query: str, faiss_index: FAISS):
    docs = retrieve_documents(query, faiss_index, k = 7)
    return [doc.page_content for doc in docs]

def evaluate_documents(query: str, documents: List[str]) -> List[float]:
    """
    Evaluate the relevance of documents based on a query.

    Args:
        query (str): The query string.
        documents (List[str]): A list of document contents to evaluate.

    Returns:
        List[float]: A list of relevance scores for each document.
    """

    return [retrieval_evaluator_chain(query, doc) for doc in documents]

def generate_response(query: str, knowledge: str):
   
    return generate_response_chain(query, knowledge)


def crag_process(question: str, faiss_index: FAISS):
    """
        Process a question by retrieving, evaluating, and using documents 
        or performing a web search to generate a response.

        Args:
            question (str): The query string to process.
            faiss_index (FAISS): The FAISS index used for document retrieval.

        Returns:
            str: The generated response based on the query.
    """

    logging.info("Started CRAG process")

    # Retrieve and Evaluate documents
    retrieved_documents = retrieve_docs(question, faiss_index)
    eval_scores = evaluate_documents(question, retrieved_documents)

    logging.info(f"\nRetrieved {len(retrieved_documents)} documents")
    logging.info(f"Evaluation scores: {eval_scores}")

    max_score = max(eval_scores)
    sources = []

    if max_score > 0.7:
        logging.info("Action: Correct - Using retrieved documents")
        best_doc = retrieved_documents[eval_scores.index(max_score)]
        final_knowledge = best_doc
        sources.append(("Retrieved document", ""))
    elif max_score < 0.3:
        logging.info("Action: Incorrect - Performing web search")
        final_knowledge = perform_web_search(question)
    else:
        logging.info("Action: Ambiguous - Combining retrieved document and web search")
        best_doc = retrieved_documents[eval_scores.index(max_score)]
        retrieved_knowledge = knowledge_refinment(best_doc)
        web_knowledge = perform_web_search(question)
        final_knowledge = "\n".join(retrieved_knowledge + web_knowledge)
        sources = [("Retrieved document", "")]

    answer = generate_response(question, final_knowledge)

    return question, answer

    

