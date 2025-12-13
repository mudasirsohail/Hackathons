import React from 'react';
import ChatWidget from './ChatWidget';

// Root component that wraps the entire application
const Root = ({ children }) => {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
};

export default Root;