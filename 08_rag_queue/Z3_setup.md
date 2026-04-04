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

---

# Notes: FastAPI + RQ based RAG query system

This part explains the backend flow from your `server.py` and `worker.py` files.

## 8) What this layer does

This layer is used to accept a user query through an API, send that query to a background job queue, search the vector database, and return the final answer.

The flow is:

**FastAPI server → RQ queue → worker → Qdrant search → OpenAI response → job result**

---

## 9) FastAPI setup

FastAPI is used to create the API server.

Install FastAPI with the standard extras:

```bash
pip install "fastapi[standard]"
```

Why this step matters:

* It gives you FastAPI with useful standard dependencies.
* It helps you build API endpoints quickly.
* It works well for small and large backend apps.

---

## 10) RQ setup

RQ (Redis Queue) is used to push the query into a background job.

Install RQ:

```bash
pip install rq
pip freeze > requirements.txt
```

Why this step matters:

* It lets long-running tasks run in the background.
* It prevents the API from freezing while the answer is being generated.
* It is useful when query processing takes time.

RQ is designed around three main ideas: `Queue`, `Job`, and `Worker`.

---

## 11) `server.py` explanation

This file creates the FastAPI app and exposes the API endpoints.

### `load_dotenv()`

This loads environment variables from a `.env` file.

It is useful for keeping API keys and private configuration outside the code.

### `app = FastAPI()`

This creates the FastAPI application object.

### `GET /`

This route checks whether the server is running.

It returns a simple status message:

```python
{"status": "Server is up and running"}
```

### `POST /chat`

This route accepts a query from the user and sends it to the queue.

```python
job = queue.enqueue(process_query, query)
```

What happens here:

* The query is placed into the Redis queue.
* RQ creates a job.
* The worker will pick up this job later.
* The API immediately returns the job ID.

### `GET /job-status`

This route checks the result of a queued job.

It uses the job ID to fetch the job and then returns the generated answer.

Why this is useful:

* The user can submit a query first.
* Then the user can check the result later.
* This keeps the API responsive.

---

## 12) `worker.py` explanation

This file contains the actual query-processing logic.

### `OpenAIEmbeddings`

This creates the embedding model used to convert the user query into vector form.

### `QdrantVectorStore.from_existing_collection(...)`

This connects to an already created Qdrant collection.

It means the PDF chunks were already indexed earlier and are now available for retrieval.

### `process_query(query)`

This function does the real work.

#### Step 1: Search the vector database

The query is searched against Qdrant:

```python
search_results = vector_db.similarity_search(query=query)
```

This returns the most relevant chunks from the stored PDF data.

#### Step 2: Build context

The returned chunks are joined into one context block.

The context includes:

* page content
* page number
* source file path

#### Step 3: Create the system prompt

The system prompt tells the model to answer only from the retrieved PDF context.

This is the core RAG idea: the model should not guess from memory when the answer can be found in the document.

#### Step 4: Call OpenAI chat completion

The query and context are sent to the model:

```python
response = openai_client.chat.completions.create(...)
```

The model then generates the final answer.

#### Step 5: Return the answer

The function returns the text response, which becomes the job result.

---

## 13) Why use RQ here

RQ is helpful because query processing can take time:

* vector search
* prompt preparation
* LLM response generation

Instead of blocking the API request, the task is sent to the background worker.

---

## 14) Main execution flow

### When a user asks a question

1. The user sends a query to `/chat`.
2. FastAPI sends the query to RQ.
3. RQ stores the task as a job.
4. A worker picks up the job.
5. The worker searches Qdrant.
6. The worker sends the retrieved chunks to OpenAI.
7. The final answer is stored as the job result.
8. The client checks `/job-status` with the job ID.

---

## 15) Run command for the main file

If your project structure is like this:

```text
rag_queue/
  main.py
  server.py
  worker.py
```

Then you can run the main file with:

```bash
python -m rag_queue.main
```

Using `python -m` runs the module from the package path instead of running the file directly.

---

## 16) Combined install summary for this backend

```bash
pip install "fastapi[standard]"
pip install rq
pip freeze > requirements.txt
```

---

## 17) Final backend summary

This backend uses FastAPI for the API layer, RQ for background job handling, Qdrant for vector search, and OpenAI for the final answer generation. The API receives the query, the worker searches the stored chunks, and the model answers using the retrieved PDF context.
