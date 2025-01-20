import React, { useState } from 'react';
import { Send } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

const AISceneGenerator = () => {
  const [prompt, setPrompt] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    setIsProcessing(true);
    try {
      // Process prompt and generate scene
      const sceneElements = await processPrompt(prompt);
      setResult(sceneElements);
    } catch (error) {
      console.error('Error generating scene:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-4 space-y-4">
      <div className="flex flex-col space-y-2">
        <h2 className="text-2xl font-bold">SceneX AI Scene Generator</h2>
        <p className="text-gray-600">
          Describe your cloud/network/AI architecture in natural language
        </p>
      </div>

      <div className="flex space-x-2">
        <textarea
          className="flex-1 min-h-[100px] p-2 border rounded-lg"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Example: Create a serverless ML inference pipeline with API Gateway, Lambda, and SageMaker endpoints..."
        />
        <button
          onClick={handleSubmit}
          disabled={isProcessing || !prompt.trim()}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50"
        >
          {isProcessing ? (
            <span>Processing...</span>
          ) : (
            <div className="flex items-center space-x-2">
              <Send size={16} />
              <span>Generate</span>
            </div>
          )}
        </button>
      </div>

      {result && (
        <Alert>
          <AlertDescription>
            Scene generated! Elements: {JSON.stringify(result)}
          </AlertDescription>
        </Alert>
      )}
    </div>
  );
};

const processPrompt = async (prompt) => {
  // This would connect to your scene generation logic
  return {
    components: [],
    connections: [],
    animations: []
  };
};

export default AISceneGenerator;