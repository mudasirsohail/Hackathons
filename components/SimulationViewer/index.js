/**
 * SimulationViewer Component
 * 
 * A component to embed and display simulation content
 */
import React from 'react';

const SimulationViewer = ({ src, title, description }) => {
  return (
    <div className="container margin-vert--md">
      <div className="card">
        <div className="card__header">
          <h3>{title || 'Simulation Viewer'}</h3>
        </div>
        <div className="card__body">
          {description && <p>{description}</p>}
          <div className="embed-responsive embed-responsive-16by9">
            <iframe 
              src={src} 
              title={title}
              width="100%" 
              height="400px"
              frameBorder="0"
              allowFullScreen
            ></iframe>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimulationViewer;