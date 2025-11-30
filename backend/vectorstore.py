from typing import List
from langchain_community.vectorstores import FAISS
from constants import PATH

def build_or_update_vector_db(chunks, embeddings, path = PATH):
    try:
        db = FAISS.load_local(path, embeddings, allow_dangerous_deserialization = True)
        db.add_documents(chunks)
    except:
        db = FAISS.from_documents(chunks, embeddings)

    db.save_local(path)
    return db

def load_vector_db(embeddings, path):
    db = FAISS.load_local(path, embeddings, allow_dangerous_deserialization = True)
    return db

def retrieve_documents(query: str, faiss_index: FAISS, k: int = 3) -> List[str]:
    """
        Retrieve documents based on a query using a FAISS index.

        Args:
            query (str): The query string to search for.
            faiss_index (FAISS): The FAISS index used for similarity search.
            k (int): The number of top documents to retrieve. Defaults to 3.

        Returns:
            List[str]: A list of the retrieved document contents.
    """

    docs = faiss_index.similarity_search(query, k = k)
    return docs
    