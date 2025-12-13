const fs = require('fs').promises;
const path = require('path');
const { QdrantClient } = require('@qdrant/js-client-rest');
const Cohere = require('cohere-ai');

// Initialize Qdrant client
const qdrantClient = new QdrantClient({
  url: process.env.QDRANT_URL || 'https://ea974bce-cce4-410c-8590-f4db3dcadddf.europe-west3-0.gcp.cloud.qdrant.io:6333',
  apiKey: process.env.QDRANT_API_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.NcgCBFjNKxKw4d31n2DVbT34vJMYAZ4AMogom33nYRU',
});

// Initialize Cohere client for newer SDK versions
const cohereClient = new Cohere.CohereClient({
  token: process.env.COHERE_API_KEY || 'uFamLMi8dv2qlYxDBHF2D47pICxrQhrGFT9sbP1I',
});

const COLLECTION_NAME = 'robotics_docs';

/**
 * Extract text content from markdown files recursively
 */
async function extractMarkdownFiles(dirPath) {
  const entries = await fs.readdir(dirPath, { withFileTypes: true });
  let filePaths = [];

  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);

    if (entry.isDirectory()) {
      const subPaths = await extractMarkdownFiles(fullPath);
      filePaths = filePaths.concat(subPaths);
    } else if (path.extname(entry.name) === '.md') {
      filePaths.push(fullPath);
    }
  }

  return filePaths;
}

/**
 * Clean and preprocess markdown content
 */
function cleanMarkdownContent(content) {
  // Remove frontmatter if present
  const frontmatterRemoved = content.replace(/^---[\s\S]*?---/, '');
  
  // Remove markdown formatting and clean content
  return frontmatterRemoved
    .replace(/```[\s\S]*?```/g, '') // Remove code blocks
    .replace(/`[^`]*`/g, '')        // Remove inline code
    .replace(/\*\*(.*?)\*\*/g, '$1') // Remove bold
    .replace(/\*(.*?)\*/g, '$1')    // Remove italic
    .replace(/!\[.*?\]\(.*?\)/g, '') // Remove image tags
    .replace(/\[(.*?)\]\(.*?\)/g, '$1') // Remove links, keep text
    .replace(/#{1,6}\s+/g, '')      // Remove headers markdown
    .replace(/^\s*[-*_]\s*$/gm, '') // Remove horizontal rules
    .replace(/\n\s*\n/g, '\n\n')    // Normalize newlines
    .trim();
}

/**
 * Chunk documents into smaller pieces
 */
function chunkDocument(text, maxChunkSize = 1000, overlap = 200) {
  const chunks = [];
  const paragraphs = text.split('\n\n').filter(p => p.trim() !== '');
  
  let currentChunk = '';
  
  for (const paragraph of paragraphs) {
    if (currentChunk.length + paragraph.length <= maxChunkSize) {
      currentChunk += paragraph + '\n\n';
    } else {
      // If even a single paragraph is too large, split it into sentences
      if (paragraph.length > maxChunkSize) {
        const sentences = paragraph.match(/[^\.!?]+[\.!?]+/g) || [paragraph];
        
        for (const sentence of sentences) {
          if (currentChunk.length + sentence.length <= maxChunkSize) {
            currentChunk += sentence + ' ';
          } else {
            if (currentChunk.trim()) {
              chunks.push(currentChunk.trim());
              // Create overlapping chunk if possible
              const overlapText = currentChunk.slice(-overlap).split(' ').slice(1).join(' ');
              currentChunk = overlapText + ' ' + sentence + ' ';
            } else {
              currentChunk = sentence + ' ';
            }
          }
        }
      } else {
        if (currentChunk.trim()) {
          chunks.push(currentChunk.trim());
          // Create overlapping chunk
          const overlapText = currentChunk.slice(-overlap).split(' ').slice(1).join(' ');
          currentChunk = overlapText + ' ' + paragraph + '\n\n';
        } else {
          currentChunk = paragraph + '\n\n';
        }
      }
    }
  }
  
  if (currentChunk.trim()) {
    chunks.push(currentChunk.trim());
  }
  
  return chunks;
}

/**
 * Index documents to Qdrant
 */
async function indexDocuments() {
  try {
    console.log('Starting document indexing...');
    
    // Extract all markdown files from docs directory
    const docsPath = path.join(__dirname, '../docs');
    const markdownFiles = await extractMarkdownFiles(docsPath);
    
    console.log(`Found ${markdownFiles.length} markdown files to process`);
    
    let pointId = 0;
    const points = [];
    
    for (const filePath of markdownFiles) {
      console.log(`Processing file: ${filePath}`);
      
      // Read the file content
      const content = await fs.readFile(filePath, 'utf8');
      const cleanedContent = cleanMarkdownContent(content);
      
      // Create chunks
      const chunks = chunkDocument(cleanedContent);
      
      // Generate embeddings for each chunk
      for (const [chunkIndex, chunk] of chunks.entries()) {
        if (!chunk.trim()) continue; // Skip empty chunks
        
        try {
          console.log(`Embedding chunk ${chunkIndex + 1}/${chunks.length} of ${path.basename(filePath)}`);
          
          // Generate embedding using Cohere
          const response = await cohereClient.embed({
            texts: [chunk],
            model: 'embed-english-v3.0',
            inputType: 'search_document',
          });

          const embedding = response.embeddings[0];
          
          // Create a point for Qdrant
          points.push({
            id: pointId++,
            vector: embedding,
            payload: {
              content: chunk,
              source: filePath.replace(path.join(__dirname, '..'), ''),
              fileName: path.basename(filePath),
              chunkIndex,
            },
          });
        } catch (embedError) {
          console.error(`Error embedding chunk from ${filePath}:`, embedError.message);
          continue;
        }
      }
    }
    
    if (points.length === 0) {
      console.log('No points to upload. Exiting.');
      return;
    }
    
    console.log(`Uploading ${points.length} points to Qdrant...`);
    
    // Upload points to Qdrant
    await qdrantClient.upsert(COLLECTION_NAME, {
      wait: true, // Wait for operation to complete
      points,
    });
    
    console.log(`${points.length} documents indexed successfully.`);
  } catch (error) {
    console.error('Error indexing documents:', error);
    throw error;
  }
}

if (require.main === module) {
  indexDocuments()
    .then(() => {
      console.log('Document indexing complete.');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Failed to index documents:', error);
      process.exit(1);
    });
}

module.exports = { indexDocuments };