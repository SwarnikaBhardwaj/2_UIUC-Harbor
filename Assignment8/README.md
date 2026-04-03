# Harbor RAG System – Assignment 8

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system for the Harbor student marketplace concept. Harbor is a campus-focused platform where students can advertise services such as tutoring, photography, beauty services, and fundraisers to other students within the university community.

The RAG system allows users to ask natural language questions about the marketplace listings and receive responses grounded in the actual service descriptions stored in the dataset.

System pipeline:

User → Query → Embedding → Vector Search → Retrieved Context → LLM → Response

---

## Dataset Requirement

To run this project, you must have the **Illinois Campus Marketplace dataset** used as the knowledge base.

The dataset contains the student service listings that the RAG system retrieves from when answering questions.

If running in Google Colab, the dataset must be **uploaded manually into the runtime environment** before executing the notebook.

---

## Recommended Runtime Environment

The notebook runs best in **Google Colab**.

Recommended configuration:

- Python Runtime: Python 3
- Hardware Accelerator: **T4 GPU**

A T4 GPU runtime is available in Google Colab and can typically be accessed when logged in with a university email account.

To enable the runtime:

Runtime → Change Runtime Type → Hardware Accelerator → **T4 GPU**

---

## How to Run the Project

1. Open `rag_system.ipynb` in **Google Colab**
2. Upload the Illinois Campus Marketplace dataset when prompted
3. Run all notebook cells sequentially

The notebook will:

- Load the marketplace dataset
- Apply chunking strategies
- Generate embeddings using three embedding models
- Perform similarity-based retrieval
- Generate responses using the language model
- Run evaluation experiments and benchmarking

---

## Runtime Expectations

When running the notebook in Google Colab with the recommended GPU configuration, the full pipeline takes approximately:

**8–10 minutes**

This includes:

- loading embedding models
- generating embeddings
- running retrieval experiments
- generating benchmark outputs

Runtime may vary slightly depending on available Colab resources.

---

## Models Used

### Embedding Models

| Model Size | Model |
|---|---|
| Small | sentence-transformers/all-MiniLM-L6-v2 |
| Medium | sentence-transformers/all-mpnet-base-v2 |
| Large | BAAI/bge-large-en-v1.5 |

### Generation Model

Qwen/Qwen2.5-3B-Instruct

This model generates the final responses based on the retrieved marketplace listings.

---

## Notes

- The notebook must run **end-to-end without errors**.
- The dataset must be uploaded manually when running in Colab.
- Relative paths are used so the notebook can run across different environments.
