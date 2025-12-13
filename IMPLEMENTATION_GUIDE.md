# RAG Chatbot Implementation Guide

This document details the implementation of the Retrieval-Augmented Generation (RAG) chatbot for the "Physical AI & Humanoid Robotics" book.

## Architecture Overview

The RAG chatbot consists of the following components:

1. **Frontend Chat Widget** - A React component integrated into the Docusaurus layout
2. **FastAPI Backend** - Handles chat requests and RAG processing
3. **Qdrant Vector Database** - Stores document embeddings for retrieval
4. **Cohere Embeddings** - Generates vector representations of text
5. **Google Gemini** - Generates responses based on retrieved context

## Features

- General questions about the book content using RAG retrieval
- Context-specific questions using selected text on the page
- Visual feedback for selected text
- Source attribution for responses

## Frontend Implementation

- Located in `src/components/ChatWidget.jsx`
- Captures selected text using mouse and keyboard event listeners
- Displays selected text preview in the chat interface
- Includes a button to automatically prepend selected text to the query

## Backend Implementation

- Located in `backend/main.py`
- FastAPI application with `/chat` endpoint
- Processes queries with or without selected text context
- Uses Cohere for embeddings and Qdrant for retrieval
- Generates responses using Google Gemini

## Data Pipeline

- Document indexing script in `backend/index_documents.py`
- Automatically processes all markdown files in the `docs` directory
- Splits documents into overlapping chunks
- Embeds chunks and stores them in Qdrant

## Environment Variables

Required environment variables (stored in `.env`):

```
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
GEMINI_API_KEY=your_gemini_api_key
COHERE_API_KEY=your_cohere_api_key
```

## Setup Instructions

1. Install Python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Set up environment variables in `.env` file

3. Index the documents:
   ```bash
   python backend/index_documents.py
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```

5. Update the Docusaurus config to point to your backend:
   - Modify the `docusaurus.config.js` to set API_CONFIG.baseUrl to your backend URL

## How to Use

1. Select text in the book content
2. The chat widget will show a preview of the selected text
3. Use the "+" button to prepend the selected text to your query
4. Submit your question
5. The chatbot will respond based only on the selected text context

## Troubleshooting

- Ensure all API keys are correctly configured
- Verify Qdrant collection exists and contains document embeddings
- Check that the backend is properly connected to all services