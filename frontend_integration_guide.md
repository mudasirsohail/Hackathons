# Frontend Integration Guide: RAG Chatbot for Docusaurus

## Overview
This guide explains how to integrate the RAG chatbot into your Docusaurus documentation site. The integration includes a React component that connects to the FastAPI backend.

## Prerequisites
- Docusaurus 2.x project
- Basic knowledge of React
- A running instance of the backend API

## Step-by-Step Integration

### 1. Install the Chat Component
1. Create a `components` directory in your Docusaurus `src` folder if it doesn't exist:
   ```
   src/
   └── components/
       ├── ChatInterface.js
       └── ChatInterface.css
   ```

2. Copy the `ChatInterface.js` and `ChatInterface.css` files you created to this directory.

### 2. Add the Chat Component to Your Layout

#### Option A: Add to All Pages (Global Chat)
To add the chatbot to all pages, modify your theme configuration in `docusaurus.config.js`:

```js
// docusaurus.config.js
module.exports = {
  // ... your existing config
  themes: [
    // ... your existing themes
  ],
  plugins: [
    // ... your existing plugins
  ],
  themeConfig: {
    // ... your existing theme config
    navbar: {
      // ... your existing navbar config
    },
    footer: {
      // ... your existing footer config
    },
  },
};

// To add the chat to all pages, you can wrap your app in App.js
// or use a layout override
```

For a global chat overlay, create `src/theme/Layout/index.js`:

```js
import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatInterface from '@site/src/components/ChatInterface';
import { useState, useEffect } from 'react';

export default function Layout(props) {
  const [showChat, setShowChat] = useState(false);

  // Show chat button on all pages
  useEffect(() => {
    // Add any initialization logic here
  }, []);

  return (
    <>
      <OriginalLayout {...props}>
        {props.children}
      </OriginalLayout>
      
      {/* Floating Chat Button */}
      <button 
        className="floating-chat-btn" 
        onClick={() => setShowChat(!showChat)}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          zIndex: 1000,
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          fontSize: '24px',
          cursor: 'pointer',
          boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
        }}
      >
        💬
      </button>
      
      {/* Chat Interface - only show when toggled */}
      {showChat && (
        <div 
          style={{
            position: 'fixed',
            bottom: '90px',
            right: '20px',
            width: '400px',
            height: '600px',
            zIndex: 1000,
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
          }}
        >
          <ChatInterface docsDir="/docs" />
        </div>
      )}
    </>
  );
}
```

#### Option B: Add to Specific Pages
To add the chat to specific pages like your documentation index, edit the relevant MDX file:

```md
<!-- In your docs/index.md or any other MDX file -->
import ChatInterface from '@site/src/components/ChatInterface';

# Welcome to My Documentation

This is my documentation site with an integrated RAG chatbot.

<ChatInterface docsDir="/docs" />
```

### 3. Configure the Backend API Endpoint
In the `ChatInterface.js` component, ensure the API endpoint matches your backend:

```js
// Update this line in ChatInterface.js with your actual backend URL
const response = await fetch('https://mudasirsohail-physical-ai-backend-2edf874.hf.space/chat', {
```

For production, you'll likely want to make this configurable:

```js
// In docusaurus.config.js, add a custom field
customFields: {
  chatApiUrl: process.env.CHAT_API_URL || 'https://mudasirsohail-physical-ai-backend-2edf874.hf.space'
}
```

Then in your component:
```js
// Read the config in your component
const chatApiUrl = window.chatApiUrl || 'https://mudasirsohail-physical-ai-backend-2edf874.hf.space';
```

### 4. Enable Text Selection Feature
The chat interface can work in two modes:
- **Global Mode**: Searches through all documentation
- **Selected Text Mode**: Focuses only on user-selected text

The component automatically detects text selection. To ensure this works properly:

1. Make sure your documentation content allows text selection
2. The component listens to mouseup events to detect selections

### 5. Environment Configuration
Add environment variables for the API endpoints:

```bash
# In your deployment environment
CHAT_API_URL=https://mudasirsohail-physical-ai-backend-2edf874.hf.space
```

For local development, you can add to a `.env.local` file in your Docusaurus directory:
```
CHAT_API_URL=https://mudasirsohail-physical-ai-backend-2edf874.hf.space
```

### 6. Styling and Customization
The component includes default styles, but you can customize:
- Colors to match your brand
- Positioning (floating vs. embedded)
- Size and responsiveness

## Using the Chat Component

### Props
- `docsDir`: Path to your documentation directory (default: "/docs")

### Features
1. **Global Search**: Asks questions about all documentation
2. **Selected Text Focus**: Answers questions about highlighted text
3. **Chat History**: Maintains conversation history within a session
4. **Loading States**: Shows when the AI is processing
5. **Error Handling**: Graceful degradation if API is unavailable

## Deployment
1. Ensure your backend API is deployed and accessible
2. Configure the appropriate API URLs for your environment
3. Test the chat functionality across different pages and devices
4. Monitor API usage to ensure your free-tier limits aren't exceeded

## Troubleshooting

### Common Issues:
1. **CORS Errors**: Ensure your FastAPI backend allows requests from your Docusaurus domain
2. **API Not Responding**: Check that your backend service is running and accessible
3. **Text Selection Not Working**: Verify that text selection events are not being intercepted

### CORS Configuration
In your FastAPI backend (`app/main.py`), ensure CORS is properly configured:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Security Considerations
1. Use HTTPS for production deployments
2. Implement rate limiting on your backend API
3. Consider adding authentication if sensitive information is involved
4. Validate and sanitize all inputs on the backend

## Performance Optimization
1. Implement caching for frequent queries
2. Use pagination for large chat histories
3. Optimize embedding models and vector searches
4. Consider CDN for static assets