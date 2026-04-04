# Notes: Local RAG Setup with Docker Compose

## 1) What you are building

You are building a **local vector database setup** for Retrieval-Augmented Generation (RAG). In this setup, your PDF data is converted into vector embeddings and stored in a vector database so it can be searched later.

---

## 2) Local vector DB setup with Docker Compose

1. Open Docker and make sure it is running.
2. Create a folder, for example `rag`.
3. Inside `rag`, create a file named `docker-compose.yml`.
4. Run the Docker Compose command from inside that folder.

Example:

```bash
docker compose up -d
```

`-d` means detached mode, so the container keeps running in the background. If you run Compose in attached mode, pressing `Ctrl+C` can stop the containers.

To stop the stack later:

```bash
docker compose down
```

---

## 3) Indexing phase

Indexing is the process of preparing your data so it can be searched later. The flow is:

**PDF file → chunks → embeddings → vector database**

This is the phase where your document data becomes searchable.

### 3.1 Loading the PDF

First, load the PDF file into your application.

Install the required packages:

```bash
pip install -U langchain-community pypdf
pip freeze > requirements.txt
```

Why this step matters:

* It reads the PDF content.
* It converts the PDF into document objects.
* It prepares the text for splitting and embedding.

---

### 3.2 Chunking the text

After loading the PDF, split the text into smaller parts called **chunks**.

Install the text splitter package:

```bash
pip install -U langchain-text-splitters
pip freeze > requirements.txt
```

Why this step matters:

* Large documents are too big to send as one block.
* Smaller chunks improve search quality.
* Each chunk can later be matched with user queries more accurately.

---

### 3.3 Creating embeddings for the chunks

Next, convert each chunk into a vector embedding.

Install the embedding package:

```bash
pip install -U langchain-openai
```

Why this step matters:

* Embeddings convert text into numbers.
* Similar meanings produce similar vectors.
* This makes semantic search possible.

---

### 3.4 Storing vectors in Qdrant

Now store the embeddings in Qdrant, which is your vector database.

Install the Qdrant integration:

```bash
pip install -U langchain-qdrant
```

Why this step matters:

* The vector database stores all chunk embeddings.
* It allows fast similarity search.
* It helps the system find the most relevant text later.

---

## 4) Retrieval phase

Retrieval is the part where the user asks a question and the system searches the stored vectors to find the best matching chunks.

### Retrieval flow

1. The user gives a query.
2. The query is converted into an embedding.
3. Qdrant searches for similar vectors.
4. The top matching chunks are returned.
5. These chunks are sent to the language model as context.
6. The model generates the final answer.

### Why retrieval matters

Without retrieval, the model only depends on what it already knows or what fits into the prompt window. With retrieval, the model can answer using your own PDF content, which makes the answer more accurate and specific.

---

## 5) Full pipeline summary

**PDF loading → chunking → embeddings → Qdrant storage → user query → query embedding → similarity search → retrieved chunks → final answer**

---

## 6) Command summary

```bash
# Docker stack
docker compose up -d
docker compose down

# PDF loading
pip install -U langchain-community pypdf
pip freeze > requirements.txt

# Chunking
pip install -U langchain-text-splitters
pip freeze > requirements.txt

# Embeddings
pip install -U langchain-openai

# Vector DB integration
pip install -U langchain-qdrant
```

---

## 7) Final note

This setup gives you a simple local RAG pipeline. First, your PDF is prepared and stored as vectors. Then, when a user asks a question, the system retrieves the most relevant chunks and uses them to answer.
