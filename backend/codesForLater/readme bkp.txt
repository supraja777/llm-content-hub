# LLM Data Ingestion & Vectorization Pipeline

This repository contains a robust pipeline for crawling, processing, and vectorizing web content. The pipeline is designed for **daily ingestion of new content**, deduplication, chunking, and storage in a **FAISS vector database** for downstream retrieval-augmented generation (RAG) or other LLM tasks.

---

---

## Pipeline Workflow

```mermaid
flowchart TD
    A[Start: Load Existing URLs] --> B[Crawl Blog for All Links]
    B --> C[Filter New URLs]
    C --> D[Save New URLs to stored_urls.json]
    D --> E{New URLs Exist?}
    E -->|No| F[Log: No new URLs]
    E -->|Yes| G[Load Documents in Batches]
    G --> H[Chunk Documents]
    H --> I[Generate Embeddings]
    I --> J[Insert/Update FAISS Vector Store]
    J --> K[Pipeline Complete]
```
---

## Features

- **Web Crawling:** Automatically fetches new articles from the target blog.
- **Deduplication:** Filters out previously stored URLs.
- **Batch Processing:** Loads documents in batches to avoid memory spikes.
- **Text Chunking:** Splits long documents into smaller chunks for embeddings.
- **Embeddings:** Uses HuggingFace `sentence-transformers/all-MiniLM-L6-v2`.
- **Vector Storage:** Stores chunks in FAISS with incremental updates.
- **Logging:** Tracks pipeline progress and errors for easy debugging.
- **Extensible:** Can add new sources, custom chunking, or embeddings easily.

---

## How to Run

1. **Install dependencies:**

```bash
pip install -r requirements.txt
````

2. **Run the pipeline:**

```bash
python main.py
```

* The script will crawl the blog, filter new URLs, load documents, chunk them, generate embeddings, and insert them into FAISS.

---

## Configuration

| Constant        | Description                           |
| --------------- | ------------------------------------- |
| `BASE_URL`      | Blog homepage to crawl                |
| `BATCH_SIZE`    | Number of documents processed at once |
| `CHUNK_SIZE`    | Size of each text chunk in characters |
| `CHUNK_OVERLAP` | Overlap between consecutive chunks    |

---

## **FAISS Vector Store Document Structure**

Each document stored in FAISS has the following structure:

```python
Document(
    id='unique-id',
    metadata={
        'source': 'https://example.com/article-url',
        'title': 'Title of the Article',
        'description': 'Short description of content',
        'language': 'en',
        'fetched_at': 'YYYY-MM-DD'
    },
    page_content='Full text content of the chunked document'
)
```

**Example documents from the pipeline:**

```python
[
    Document(
        id='849761d4-fc5b-48bd-9be6-274cd5011ee1',
        metadata={
            'source': 'https://ragyfied.com/articles/attention-is-all-you-need-explained',
            'title': 'How Large Language Models Work: Understanding Attention and Transformers | RAGyfied',
            'description': 'A clear, intuitive explanation of how LLMs like GPT-4 and GPT-5 actually work under the hood — with focus on attention.',
            'language': 'en',
            'fetched_at': '2025-11-28'
        },
        page_content='How Large Language Models Work: Understanding Attention and Transformers...'
    ),
    Document(
        id='16231cc1-2f47-4dda-9d86-e1418a101c23',
        metadata={
            'source': 'https://ragyfied.com/articles/what-is-embedding-in-ai',
            'title': 'Understanding Embeddings: The Secret Language of Meaning in AI | RAGyfied',
            'description': 'A practical deep dive into what embeddings really are, how they are created, stored, and scaled.',
            'language': 'en',
            'fetched_at': '2025-11-28'
        },
        page_content='Example:\nA multilingual model may group “perro” near “dog”...'
    ),
    Document(
        id='e030fd01-2553-4361-87dd-cef75a635ed7',
        metadata={
            'source': 'https://ragyfied.com/articles/what-is-transformer-architecture',
            'title': 'Deconstructing the Giants: A Technical Deep Dive into LLM Architecture, Performance, and Cost | RAGyfied',
            'description': 'Technical breakdown of Transformer architecture: understand LLM parameters, VRAM requirements, latency, and deployment costs.',
            'language': 'en',
            'fetched_at': '2025-11-28'
        },
        page_content='The headline specification of a Large Language Model (LLM)—be it 7B, 70B, or 175B—is its parameter count...'
    ),
    # ...more documents
]
```

* `id`: unique identifier for the document/chunk
* `metadata.source`: URL of the original article
* `metadata.title`: article title
* `metadata.description`: short summary or snippet
* `metadata.language`: content language
* `metadata.fetched_at`: date of ingestion (`YYYY-MM-DD`)
* `page_content`: actual text content of the chunk

> All documents are **chunked** and **embedded**, allowing for semantic search via FAISS.



---

## Future Enhancements

* Parallel document loading for faster ingestion.
* Retry mechanism for failed URL loads.
* Metadata tracking (author, timestamp, source URL) for chunks.
* Multi-source ingestion: RSS feeds, newsletters, other blogs.
* Alerts or notifications for pipeline failures or new data ingestion.

---

## Example Logging Output

```
INFO: Loaded batch 1 of 3
INFO: Created chunks
INFO: Inserted chunks into FAISS vector store
INFO: Pipeline complete
```

---
---

## **LLM Updates Retrieval Pipeline**

This pipeline retrieves **today’s latest updates** from the FAISS vector store for a given topic and aggregates them using an LLM. It is designed to filter content by ingestion date and summarize it for display.

---

### **Pipeline Workflow**

```mermaid
flowchart TD
    A[Start: User selects topic/query] --> B[Load FAISS Vector Store]
    B --> C[Perform similarity search using query]
    C --> D[Filter documents by today's date]
    D --> E[Aggregate & summarize content using LLM]
    E --> F[Optional: Fact-check summaries using LLM or external sources]
    F --> G[Return latest updates to user]
```

---

### **Pipeline Steps**

1. **User selects a topic/query**
   Example: `"Latest updates on Large Language Models"`

2. **Retrieve documents from FAISS vector store**

   * Similarity search returns top `k` relevant documents.
   * Filter only documents with `fetched_at` equal to today’s date.

3. **Aggregate and summarize content**

   * Each document is summarized using an LLM.
   * Aggregated list pairs the source URL with its summary.

4. **Optional fact-checking**

   * Future enhancement: validate correctness and reduce hallucinations.

5. **Return aggregated summaries to the user**

---

### **Features**

* Retrieves **today’s latest content** for a given query.
* Filters documents using `fetched_at` metadata.
* Summarizes documents via LLM.
* Ready for **fact-checking extension**.
* Uses the same FAISS vector store and embeddings as the ingestion pipeline.

---

### **Example Output**

```
Source: https://ragyfied.com/articles/attention-is-all-you-need-explained
Summary: Clear, intuitive explanation of attention mechanism in LLMs like GPT-4/5...
Source: https://ragyfied.com/articles/what-is-embedding-in-ai
Summary: Practical overview of embeddings, how they are created, stored, and scaled...
```

---

# 🧠 Mock Interview Pipeline — Intelligent Questioning, Routing, and CRAG-Enhanced Answering

The **Mock Interview Pipeline** is an automated interview simulation system that generates domain-specific questions, routes each question through an intelligent decision layer, retrieves or generates knowledge using **CRAG (Corrective Retrieval-Augmented Generation)**, and produces high-quality, fact-checked answers.

This pipeline is designed for **LLM-first evaluation**, **retrieval-enhanced reasoning**, and **adaptive knowledge grounding**, making it ideal for interview prep, skill assessment, and educational tutoring applications.

---

## 🚀 End-to-End Workflow Overview

```mermaid
flowchart TD

A[📌 Select Topic] --> B[❓ Question Generator<br/>Generate interview questions + difficulty tags]

B --> C[⚖️ Router Chain<br/>Decide: LLM_ONLY vs VECTOR_DB]

C -->|LLM_ONLY| D[🤖 Direct LLM Answer Generation]

C -->|VECTOR_DB| E[🔍 CRAG Pipeline]

E --> F1[📥 Retrieve Top-k Docs]
E --> F2[🧮 Evaluate Document Relevance]
E --> F3[🔧 Decide: Correct / Ambiguous / Incorrect]
F3 -->|Correct| F4[Use Best Document]
F3 -->|Ambiguous| F5[Combine Doc + Web Search]
F3 -->|Incorrect| F6[Run Web Search Only]
F4 --> G[📝 Final Answer Generation]
F5 --> G
F6 --> G

D --> H[📤 Output Answer]
G --> H
```

---

## 🧩 Core Components

### **1. Question Generator**

* Produces high-quality topic-aligned mock interview questions.
* Each question is paired with a **difficulty label** (Easy / Medium / Hard).
* Useful for structured learning paths or interview simulations.

### **2. Router Chain (LLM-Only vs VectorDB Decision)**

The router evaluates each question and selects the optimal answering path:

* `LLM_ONLY` → Direct reasoning using model’s internal knowledge.
* `VECTOR_DB` → Requires retrieval + grounding from FAISS Index (CRAG pipeline).

This avoids unnecessary retrieval calls and speeds up inference.

#### Decision Example:

```
LLM_ONLY — The question requires general knowledge about RAG. 
The LLM can answer using its training data without vector search.
```

---

## 🛠️ The CRAG Pipeline (Corrective RAG)

CRAG enhances standard RAG by adding:

1. **Document Retrieval**
2. **Document Evaluation (Relevance Scoring)**
3. **Corrective Action Selection**
4. **Knowledge Refinement (optional)**
5. **Web Search Integration**
6. **Grounded Answer Generation**

### CRAG Decision Logic

| Condition         | Action                                                  |
| ----------------- | ------------------------------------------------------- |
| Score > 0.7       | Use retrieved document directly                         |
| Score < 0.3       | Skip retrieval → perform web search                     |
| 0.3 ≤ Score ≤ 0.7 | Combine best document + refined knowledge + web results |

---

## 📊 CRAG Process Diagram

```mermaid
flowchart LR

A[❓ Question] --> B[📥 Retrieve Documents]
B --> C[🧮 Evaluate Scores]
C --> D{Score Threshold?}

D -->|> 0.7| E1[✔ Correct<br/>Use Retrieved Doc]
D -->|< 0.3| E2[❌ Incorrect<br/>Do Web Search]
D -->|Between| E3[⚠️ Ambiguous<br/>Combine Doc + Web Knowledge]

E1 --> F[📝 Final Knowledge]
E2 --> F
E3 --> F

F --> G[🤖 Generate Grounded Answer]
```

---

## 📘 Example Outputs

### **Generated Questions**

```
("What is Retrieval-Augmented Generation and how does it enhance large language models?", "Easy")
("What are the strengths of traditional IR systems that RAG builds upon?", "Medium")
("What are the potential applications of RAG in private-data enterprise systems?", "Hard")
```

### **Router Output**

```
LLM_ONLY — The question requires general knowledge about RAG technology.
The LLM’s internal training is enough to answer it without vector search.
```

### **CRAG Decision Trace**

```
Retrieved 7 documents
Evaluation scores: [0.2, 0.8, 0.4, 0.2, 0.2, 0.0, 0.2]
Action: Correct – Using retrieved documents
```

---




