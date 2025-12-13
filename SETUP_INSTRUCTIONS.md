# RAG Chatbot Setup Instructions

Your RAG chatbot system is fully implemented with all components in place. Here's how to run it:

## 1. Environment Setup
First, create a .env file in the docs directory with your API keys:
```
GEMINI_API_KEY=AIzaSyAlceN_4DWQhYt1jy80rEkdZBdZ7FTFmNQ
QDRANT_URL=https://ea974bce-cce4-410c-8590-f4db3dcadddf.europe-west3-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.NcgCBFjNKxKw4d31n2DVbT34vJMYAZ4AMogom33nYRU
COHERE_API_KEY=uFamLMi8dv2qlYxDBHF2D47pICxrQhrGFT9sbP1I
```

## 2. Steps to Run the Complete System:

### A. Create Qdrant Collection
```bash
cd docs
node scripts/createCollection.js
```

### B. Index Your Documentation
```bash
cd docs
node scripts/indexDocs.js
```

### C. Start the API Server (in a separate terminal)
```bash
cd docs
node api/chat.js
```
This will start the API server on port 3001.

### D. Start the Docusaurus Server (in another separate terminal)
```bash
cd docs
npm run start
```
This will start the Docusaurus server on port 3000.

## 3. Using the Chatbot
- Visit http://localhost:3000/Hackathons/
- You'll see a floating chat widget in the bottom right corner
- Click on it to open the chat interface
- Ask questions about your robotics book and get answers based on the documentation

## 4. Files Created
- `/scripts/createCollection.js` - Creates Qdrant collection
- `/scripts/indexDocs.js` - Embeds markdown files using Cohere
- `/api/chat.js` - API server for the chat functionality
- `/src/components/ChatWidget.jsx` - Chat UI component
- Updated `docusaurus.config.ts` - To integrate the chat widget

The RAG (Retrieval Augmented Generation) system is fully automated and will retrieve relevant information from your documentation to answer user queries.