# RAG (Retrieval-Augmented Generation) Notes

## 1) What is RAG?

RAG means **Retrieval-Augmented Generation**.

It is a technique used to make an LLM answer using **external data** instead of relying only on its internal training knowledge.

In simple words:

- **Retrieval** = find the most relevant information from your data
- **Generation** = use the LLM to write the final answer

So, RAG connects **search + AI answer generation**.

---

## 2) What problem does RAG solve?

A normal LLM has some limitations:

- It may not know your private/company data
- It may give old or incorrect answers
- It cannot automatically read your documents, PDFs, notes, or database
- It may hallucinate, meaning it can generate answers that sound correct but are actually wrong

RAG solves these problems by letting the LLM first **retrieve relevant data** from your knowledge base, then answer based on that data.

---

## 3) How things worked before RAG

Before RAG, the usual flow was:

1. User asks a question
2. LLM generates an answer only from its training knowledge

### Limitation of this method
The model was depending only on what it had learned during training.

That means:

- It could not use your latest data
- It could not directly access your files
- It might answer with incomplete or wrong information
- Updating knowledge required retraining or fine-tuning, which is costly and slow

So, before RAG, the system was mostly:

**User query → LLM → Answer**

---

## 4) Why RAG is useful

RAG adds a knowledge retrieval layer between the user and the LLM.

This makes the system:

- more accurate
- more context-aware
- easier to update
- able to use custom data sources
- better for chat over documents, company knowledge, PDFs, and FAQs

---

# 5) RAG Pipeline

RAG works in **two main phases**:

1. **Indexing Phase** — preparing and storing data  
2. **Retrieval Phase** — answering user questions using the stored data

---

# 6) Phase 1: Indexing Phase

This is the data preparation stage.

## Goal
Convert raw data into a searchable vector format and store it in a vector database.

## Steps in indexing phase

### Step 1: Data input
First, you collect data from sources such as:

- PDF files
- web pages
- text files
- documents
- databases
- notes
- FAQs

This is the raw knowledge source for RAG.

---

### Step 2: Data chunking
The raw data is too large to send directly to the LLM, so it is split into smaller parts called **chunks**.

### Why chunking is needed
- Large documents are easier to search when broken into small sections
- Embedding models work better with smaller text pieces
- It helps retrieve only the most relevant part instead of the whole document

Example:

A big paragraph may be split into smaller chunks like:

- Chunk 1: introduction
- Chunk 2: main explanation
- Chunk 3: examples
- Chunk 4: conclusion

---

### Step 3: Embedding generation
Each chunk is passed through an **embedding model**.

The embedding model converts text into a numeric vector.

### What is a vector?
A vector is a list of numbers that represents the meaning of the text.

Similar meanings produce similar vectors.

Example:

- “How to install Docker?”  
- “Docker installation steps”

These two texts may have vectors that are close to each other because their meaning is similar.

---

### Step 4: Store in vector database
The vectors are stored in a **vector database** like:

- Qdrant
- Pinecone
- Weaviate
- FAISS

Along with the vector, the system may also store:

- original chunk text
- document name
- page number
- metadata
- source information

### Why vector database?
Because it helps find similar text very fast using vector similarity search.

---

## Indexing phase flow

**Data input → Chunking → Embedding model → Vector database**

---

# 7) Phase 2: Retrieval Phase

This is the question-answering stage.

## Goal
Take the user query, find the most relevant chunks from the vector database, and give them to the LLM for the final response.

## Steps in retrieval phase

### Step 1: User gives a query
Example:

> “What is RAG and why is it useful?”

This is the user input.

---

### Step 2: Convert query into embedding
The user query is also passed through the same embedding model.

It becomes a vector, just like the stored chunks.

This makes the query searchable in vector space.

---

### Step 3: Vector similarity search
The query vector is compared with all stored chunk vectors in the vector database.

The system finds the most similar chunks.

This is called **similarity search** or **nearest neighbor search**.

### Result
The system retrieves the most relevant chunks related to the query.

---

### Step 4: Relevant chunks are sent to the LLM
Now the retrieved chunks are given to the LLM as context.

The LLM reads:

- the user question
- the retrieved context chunks

Then it generates the final answer.

---

### Step 5: Final response
The LLM produces a response based on the retrieved information.

This makes the answer:

- more accurate
- more grounded in data
- more useful
- less likely to hallucinate

---

## Retrieval phase flow

**User query → Query embedding → Vector similarity search → Relevant chunks → LLM → Final response**

---

# 8) Full RAG flow in one view

## Indexing phase
**Raw data → Chunking → Embeddings → Vector database**

## Retrieval phase
**User query → Query embedding → Similarity search → Relevant chunks → LLM → Answer**

---

# 9) Simple example

Suppose you upload a PDF about Docker.

### During indexing:
- PDF text is extracted
- text is split into chunks
- each chunk is converted to embeddings
- embeddings are stored in Qdrant

### During retrieval:
- user asks: “How do I check Docker version?”
- query is converted into an embedding
- similar chunks about Docker commands are found
- those chunks are sent to the LLM
- LLM replies with the correct Docker version command

---

# 10) Why RAG is better than only using LLM

RAG helps because:

- it uses your own data
- it keeps answers up to date
- it reduces hallucinations
- it improves factual accuracy
- it is easier to maintain than retraining a model

---

# 11) Important terms

## Chunk
A small piece of a large document.

## Embedding
A numeric representation of text meaning.

## Vector database
A database that stores embeddings and finds similar vectors quickly.

## Similarity search
A search method that finds text with close meaning.

## LLM
A large language model that generates the final answer.

---

# 12) Final summary

RAG is a system that combines **information retrieval** with **LLM generation**.

It works in two phases:

1. **Indexing phase**  
   Raw data is split into chunks, converted into embeddings, and stored in a vector database.

2. **Retrieval phase**  
   The user query is converted into an embedding, similar chunks are retrieved, and the LLM uses them to generate the answer.

RAG is useful because it makes AI systems more accurate, more reliable, and able to answer using custom data.