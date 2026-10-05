# RAG Document Question Answering

A Retrieval-Augmented Generation (RAG) system for answering questions based on information stored in documents.

The project combines **semantic search, vector embeddings, a vector database, an LLM, semantic caching, and the Model Context Protocol (MCP)** to provide relevant and context-aware answers.

The main goal of the project is to retrieve the most relevant information from a document collection and use it as context for an LLM instead of relying only on the model's internal knowledge.

---

## Overview

Traditional LLM-based question answering has an important limitation: the model may not have access to the specific information contained in a private or specialized document collection.

RAG solves this problem by introducing a retrieval step before answer generation.

Instead of directly asking an LLM:

> "What is CMTF?"

the system first searches the document collection for relevant information about CMTF. The retrieved information is then provided to the LLM as context.

The general idea is:

**Question → Retrieve relevant information → Build context → Generate answer**

This allows the system to answer questions using information from documents that were not part of the original LLM training data.

---

## How It Works

When a user asks a question, the system first converts the question into a numerical representation called an **embedding**.

The project uses the `BAAI/bge-base-en-v1.5` embedding model.

An embedding represents the semantic meaning of a piece of text as a vector. This makes it possible to compare questions with document fragments based on meaning rather than exact words.

For example, the following questions can have similar embeddings:

* "What is CMTF?"
* "Can you explain Causal Minimal Tool Filtering?"
* "How does CMTF work?"

Even though the wording is different, they refer to the same concept.

---

## Document Retrieval

Documents are divided into smaller pieces called **chunks**.

Each chunk is converted into an embedding and stored in **Qdrant**, a vector database.

When a new question is received, its embedding is compared with the embeddings of the stored document chunks.

The system retrieves the chunks that are semantically closest to the question.

This process is called **vector search** or **dense retrieval**.

The important idea is that the system does not simply search for the same words. It searches for information that is semantically related to the question.

---

## Context Expansion

A single retrieved chunk does not always contain enough information to answer a question.

Important information can be located in neighboring chunks of the same document.

For this reason, the system can expand the retrieved result by including nearby chunks.

For example, if chunk 15 is considered highly relevant, the system can also retrieve chunks 13–17.

This provides the LLM with a larger and more coherent section of the original document.

The retrieved chunks are then combined into a context that can be passed to the language model.

---

## Reranking

Initial vector search is designed to efficiently find potentially relevant information.

However, the most similar chunks are not always the most useful ones for answering a particular question.

A reranking stage can therefore be used to reconsider the retrieved chunks and place the most relevant information first.

The process becomes:

**Vector search → Candidate chunks → Reranking → Final context**

This helps reduce irrelevant information before it reaches the LLM.

---

## Prompt Construction

After retrieval and reranking, the system has a collection of relevant document fragments.

These fragments are combined with the original question to create a prompt for the LLM.

The LLM is instructed to use the retrieved context when generating the answer.

This is an important part of the RAG approach because the model should base its response on the retrieved information rather than freely inventing an answer.

Conceptually, the prompt contains:

* the user's question;
* the retrieved document context;
* instructions describing how the context should be used.

---

## Answer Generation

The final stage is performed by a Large Language Model.

The model receives the question together with the retrieved context and generates the final answer.

The LLM therefore acts primarily as a **reasoning and generation component**, while the vector database acts as the **information retrieval component**.

This separation is one of the key principles of the system:

* **Embedding model** — represents semantic meaning;
* **Vector database** — finds relevant information;
* **Reranker** — improves relevance;
* **LLM** — generates the final response.

---

## Semantic Cache

The project also includes a **semantic cache**.

Generating an answer with an LLM can be relatively expensive and time-consuming. In addition, users may repeatedly ask the same question or slightly different versions of the same question.

For example:

> "What is TokenMizer?"

and:

> "What are the main ideas behind TokenMizer?"

may refer to very similar information.

Instead of executing the entire RAG pipeline again, the system can compare the new question with previously processed questions.

If a sufficiently similar question already exists in the semantic cache, the previously generated answer and its context can be returned.

This reduces unnecessary LLM calls and improves response time.

---

## How Semantic Cache Differs from Document Retrieval

The semantic cache and the document collection have different purposes.

The **document collection** contains the source information used to answer questions.

The **semantic cache** contains previously generated results.

In other words:

**Document collection**

> "What information exists in the documents?"

**Semantic cache**

> "Have we already answered a very similar question?"

This separation makes the retrieval process easier to understand and prevents cached answers from being treated as source documents.

---

## Semantic Cache Lifecycle

When a question is received, the system first checks whether a sufficiently similar question already exists in the cache.

If there is a cache hit, the previously generated result can be returned immediately.

If there is no suitable cached result, the normal RAG pipeline is executed.

After generating a new answer, the question, answer, and retrieved context can be stored in the semantic cache for future requests.

The overall logic is therefore:

**Question → Semantic cache → RAG retrieval if necessary → LLM → Save result**

---

## Vector Database

The project uses **Qdrant** as its vector database.

Qdrant stores both the vector representations and the metadata associated with them.

The main document collection contains information such as:

* document identifier;
* chunk index;
* chunk text;
* embedding.

The semantic cache contains information such as:

* original question;
* question embedding;
* generated answer;
* retrieved contexts.

This allows Qdrant to be used both for semantic document retrieval and for similarity-based cache lookup.

---

## Embeddings

The project uses:

**BAAI/bge-base-en-v1.5**

The model converts text into 768-dimensional vectors.

The same embedding model is used to represent user questions and document chunks.

This is important because both representations must exist in the same vector space for meaningful similarity comparisons.

The embedding model is loaded lazily and reused instead of loading its weights for every individual request.

This significantly reduces unnecessary initialization overhead.

---

## Model Context Protocol

The project also provides access to the RAG functionality through the **Model Context Protocol (MCP)**.

MCP allows external AI applications to interact with the system through defined tools.

For example, an MCP-compatible client can send a question to the RAG system without needing to know how embeddings, Qdrant, retrieval, or the LLM are implemented internally.

The client only needs to interact with the exposed MCP functionality.

This makes the RAG system easier to integrate with AI assistants and other MCP-compatible applications.

---

## Evaluation

A RAG system should not only generate answers but also provide a way to measure their quality.

The project uses **RAGAS** for RAG evaluation.

The evaluation process runs a set of predefined questions through the RAG pipeline and analyzes the resulting answers and retrieved contexts.

Possible evaluation criteria include:

### Faithfulness

Measures whether the generated answer is supported by the retrieved context.

A high faithfulness score means that the model is not introducing information that cannot be found in the retrieved documents.

### Answer Relevancy

Measures how relevant the generated answer is to the original question.

A response may be factually correct but still fail to directly answer what the user asked.

### Context Precision

Measures how much of the retrieved context is actually relevant to the question.

This helps identify cases where the retrieval system returns too much unrelated information.

### Context Recall

Measures whether the retrieved context contains the information required to answer the question.

This is particularly useful for identifying cases where the correct information exists in the document collection but was not retrieved.

---

## Why Reference Answers Are Useful

Some evaluation metrics require a reference answer or another form of ground truth.

For example, context recall requires knowledge of what information should have been retrieved in order to determine whether the retrieval process found all necessary information.

Reference answers therefore make it possible to evaluate not only whether an answer sounds reasonable, but also whether the system retrieved and used the expected information.

For retrieval-focused experiments, additional metrics such as Recall@K, Precision@K, Mean Reciprocal Rank, and Hit Rate can also be used.

---

## Main Advantages

The project combines several techniques that complement each other:

* **Semantic embeddings** allow meaning-based search.
* **Qdrant** provides efficient vector retrieval.
* **Context expansion** helps preserve information from neighboring document chunks.
* **Reranking** improves the quality of retrieved context.
* **LLM generation** produces natural-language answers.
* **Semantic caching** reduces repeated LLM requests.
* **MCP** makes the RAG functionality available to external AI clients.
* **RAGAS** provides a framework for evaluating system quality.

Together, these components form a complete document question-answering pipeline.

---

## Project Goals

The main goal of the project is to explore how modern RAG systems can combine information retrieval and language models to provide reliable answers based on external knowledge.

The project focuses on several important RAG concepts:

* document chunking;
* embedding generation;
* vector search;
* context retrieval;
* context expansion;
* reranking;
* prompt construction;
* LLM-based generation;
* semantic caching;
* MCP integration;
* RAG evaluation.

The project can also serve as a foundation for further experimentation with hybrid retrieval, advanced reranking, query rewriting, conversational memory, and automated evaluation.

---

## Future Improvements

Potential future improvements include:

* hybrid BM25 and vector retrieval;
* more advanced reranking models;
* query rewriting;
* improved context selection;
* cache expiration and invalidation;
* conversational history;
* metadata-based filtering;
* automated evaluation;
* retrieval quality analysis;
* monitoring and observability;
* API-based access to the RAG pipeline.

---

## Summary

This project implements a document question-answering system based on the RAG approach.

Instead of relying solely on the knowledge stored inside an LLM, the system first retrieves relevant information from a document collection and then provides this information to the model as context.

The addition of semantic caching reduces repeated computation, while MCP provides a convenient way to integrate the RAG system with external AI clients.

The project therefore combines **information retrieval, vector databases, embeddings, LLMs, caching, and evaluation** into a single experimental RAG system.
