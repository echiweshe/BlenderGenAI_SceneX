// src/ai/frontend/components/ScenePrompt.jsx
import React, { useState } from 'react';
import { useSceneGeneration } from '../hooks/useSceneGeneration';

const ScenePrompt = () => {
  const [prompt, setPrompt] = useState('');
  const { generateScene, isLoading } = useSceneGeneration();

  const handleSubmit = async () => {
    try {
      await generateScene(prompt);
    } catch (error) {
      console.error('Error generating scene:', error);
    }
  };

  return (
    <div className="scene-prompt-container">
      <textarea 
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Describe your architecture..."
      />
      <button 
        onClick={handleSubmit}
        disabled={isLoading}
      >
        {isLoading ? 'Generating...' : 'Generate Scene'}
      </button>
    </div>
  );
};