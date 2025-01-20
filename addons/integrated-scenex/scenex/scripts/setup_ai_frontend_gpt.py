import os

# Define base directory
base_dir = r"C:\Users\ernes\AppData\Roaming\Blender Foundation\Blender\4.2\scripts\addons\SceneX\src\ai\frontend"

# File contents
files = {
    "index.html": """<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>SceneX AI Frontend</title>
</head>
<body>
    <div id=\"root\"></div>
    <script type=\"module\" src=\"/src/index.tsx\"></script>
</body>
</html>
""",

    "package.json": """{
  \"name\": \"scenex-ai-frontend\",
  \"private\": true,
  \"version\": \"0.1.0\",
  \"type\": \"module\",
  \"scripts\": {
    \"dev\": \"vite\",
    \"build\": \"tsc && vite build\",
    \"preview\": \"vite preview\"
  },
  \"dependencies\": {
    \"@radix-ui/react-alert-dialog\": \"^1.0.5\",
    \"@radix-ui/react-slot\": \"^1.0.2\",
    \"class-variance-authority\": \"^0.7.0\",
    \"clsx\": \"^2.0.0\",
    \"lucide-react\": \"^0.263.1\",
    \"react\": \"^18.2.0\",
    \"react-dom\": \"^18.2.0\",
    \"tailwind-merge\": \"^2.0.0\",
    \"tailwindcss-animate\": \"^1.0.7\"
  },
  \"devDependencies\": {
    \"@types/node\": \"^20.8.2\",
    \"@types/react\": \"^18.2.25\",
    \"@types/react-dom\": \"^18.2.10\",
    \"@vitejs/plugin-react\": \"^4.1.0\",
    \"autoprefixer\": \"^10.4.16\",
    \"postcss\": \"^8.4.31\",
    \"tailwindcss\": \"^3.3.3\",
    \"typescript\": \"^5.2.2\",
    \"vite\": \"^4.4.11\"
  }
}
""",

    "vite.config.js": """// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
""",

    "tailwind.config.js": """// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ['class'],
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};
""",

    "src/index.tsx": """// src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/globals.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""",

    "src/styles/globals.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
""",

    "src/App.tsx": """import React from 'react';
import AISceneGenerator from './components/AISceneGenerator';

const App = () => {
  return (
    <div className=\"App\">
      <AISceneGenerator />
    </div>
  );
};

export default App;
""",

    "src/components/AISceneGenerator.tsx": """import React, { useState } from 'react';
import { Send, Loader2, Check } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const ServiceSelector = ({ onSelect }) => {
  const services = [
    { id: 'aws', name: 'AWS Services' },
    { id: 'networking', name: 'Networking' },
    { id: 'ml', name: 'Machine Learning' }
  ];

  return (
    <div className=\"grid grid-cols-3 gap-4\">
      {services.map(service => (
        <button
          key={service.id}
          onClick={() => onSelect(service)}
          className=\"p-4 border rounded-lg hover:bg-gray-50 transition-colors\"
        >
          {service.name}
        </button>
      ))}
    </div>
  );
};

const ScenePrompt = ({ onSubmit, loading }) => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = () => {
    onSubmit(prompt);
    setPrompt('');
  };

  return (
    <div className=\"space-y-4\">
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder=\"Describe your architecture (e.g., Create a serverless ML inference API with Lambda and SageMaker)...\"
        className=\"w-full h-32 p-2 border rounded-lg\"
      />
      <button
        onClick={handleSubmit}
        disabled={loading || !prompt.trim()}
        className=\"flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50\"
      >
        {loading ? (
          <Loader2 className=\"animate-spin\" size={16} />
        ) : (
          <Send size={16} />
        )}
        <span>Generate Scene</span>
      </button>
    </div>
  );
};

const GenerationStatus = ({ status }) => {
  if (!status) return null;

  return (
    <Alert>
      <AlertDescription className=\"flex items-center space-x-2\">
        <Check size={16} className=\"text-green-500\" />
        <span>Scene generated successfully!</span>
      </AlertDescription>
    </Alert>
  );
};

const AISceneGenerator = () => {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);
  const [selectedService, setSelectedService] = useState(null);

  const handleGenerate = async (prompt) => {
    setLoading(true);
    try {
      const response = await fetch('/api/generate-scene', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, service: selectedService })
      });

      const data = await response.json();
      setStatus(data);
    } catch (error) {
      console.error('Error generating scene:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className=\"w-full max-w-4xl mx-auto\">
      <CardHeader>
        <CardTitle>AI Scene Generator</CardTitle>
      </CardHeader>
      <CardContent className=\"space-y-6\">
        <ServiceSelector onSelect={setSelectedService} />
        <ScenePrompt onSubmit={handleGenerate} loading={loading} />
        <GenerationStatus status={status} />
      </CardContent>
    </Card>
  );
};

export default AISceneGenerator;
"""
}

# Function to create files
def create_files(base_path, file_structure):
    for file_name, content in file_structure.items():
        file_path = os.path.join(base_path, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

# Run the function
create_files(base_dir, files)
print("Frontend files recreated successfully!")
