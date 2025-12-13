const { QdrantClient } = require('@qdrant/js-client-rest');

// Initialize Qdrant client
const client = new QdrantClient({
  url: process.env.QDRANT_URL || 'https://ea974bce-cce4-410c-8590-f4db3dcadddf.europe-west3-0.gcp.cloud.qdrant.io:6333',
  apiKey: process.env.QDRANT_API_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.NcgCBFjNKxKw4d31n2DVbT34vJMYAZ4AMogom33nYRU',
});

const COLLECTION_NAME = 'robotics_docs';

async function createCollection() {
  try {
    // Check if collection already exists
    const collections = await client.getCollections();
    const collectionExists = collections.collections.some(col => col.name === COLLECTION_NAME);
    
    if (collectionExists) {
      console.log(`Collection "${COLLECTION_NAME}" already exists.`);
      return;
    }

    // Create collection with specified parameters
    await client.createCollection(COLLECTION_NAME, {
      vectors: {
        size: 1024, // Cohere embeddings size
        distance: 'Cosine',
      },
    });

    console.log(`Collection "${COLLECTION_NAME}" created successfully.`);
  } catch (error) {
    console.error('Error creating collection:', error);
    throw error;
  }
}

if (require.main === module) {
  createCollection()
    .then(() => {
      console.log('Collection setup complete.');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Failed to setup collection:', error);
      process.exit(1);
    });
}

module.exports = { createCollection, COLLECTION_NAME };