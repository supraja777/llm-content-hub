from langchain_text_splitters import RecursiveCharacterTextSplitter
from constants import CHUNK_OVERLAP, CHUNK_SIZE

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP,
        separators = ["\n\n", "\n", ".", "?", "!"]
    )

    return splitter.split_documents(docs)