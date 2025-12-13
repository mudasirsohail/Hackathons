/**
 * InteractiveCodeBlock Component
 * 
 * A component to display and potentially execute code examples
 */
import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

const InteractiveCodeBlock = ({ children, language, title }) => {
  return (
    <div className="container margin-vert--md">
      <div className="card">
        <div className="card__header">
          <h3>{title || 'Code Example'}</h3>
        </div>
        <div className="card__body">
          <pre>
            <code className={`language-${language}`}>
              {children}
            </code>
          </pre>
        </div>
      </div>
    </div>
  );
};

export default InteractiveCodeBlock;