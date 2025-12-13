/**
 * RoboticsDiagram Component
 * 
 * A component to display robotics diagrams and architecture images
 */
import React from 'react';
import clsx from 'clsx';

const RoboticsDiagram = ({ src, alt, caption, className }) => {
  return (
    <div className={clsx('container margin-vert--md text--center', className)}>
      <figure>
        <img 
          src={src} 
          alt={alt} 
          style={{ maxWidth: '100%', height: 'auto', border: '1px solid #ddd', borderRadius: '4px' }}
        />
        {caption && <figcaption className="margin-vert--sm">{caption}</figcaption>}
      </figure>
    </div>
  );
};

export default RoboticsDiagram;