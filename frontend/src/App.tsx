import React from 'react';
import  EnhancedChatUI  from './components/EnhancedChatUI';

// Define the interface for the chat message
interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

// Define the interface for model parameters
interface ModelParams {
  model: string;
  temperature: number;
  max_tokens: number;
  top_p: number;
  frequency_penalty: number;
  presence_penalty: number;
  stop: string[];
  stream: boolean;
  type: 'text' | 'image' | 'audio';
}

const App: React.FC = () => {
  return (
    <div className="h-screen w-screen overflow-hidden">
      <EnhancedChatUI />
    </div>
  );
};

export default App;