import React, { useState } from 'react';
import ChatHeader from './components/ChatHeader';
import MessageList from './components/MessageList';
import MessageInput from './components/MessageInput';
import SettingsModal from './components/SettingsModal';
import KnowledgeModal from './components/KnowledgeModal';
import EnhancedChat from './components/EnhancedChatUI';

interface EnhancedChatProps {
  onSettings: () => void;
  onKnowledge: () => void;
  messages: { role: string; content: string }[];
  setMessages: React.Dispatch<React.SetStateAction<{ role: string; content: string }[]>>;
  params: {
    model: string;
    temperature: number;
    max_tokens: number;
    top_p: number;
    frequency_penalty: number;
    presence_penalty: number;
    stop: string[];
    stream: boolean;
    prompt: string;
    type: 'text';
  };
  setParams: React.Dispatch<React.SetStateAction<{
    model: string;
    temperature: number;
    max_tokens: number;
    top_p: number;
    frequency_penalty: number;
    presence_penalty: number;
    stop: string[];
    stream: boolean;
    prompt: string;
    type:  'text';
  }>>;
}

// Remove this component as it's already imported from './components/EnhancedChatUI'

const App: React.FC = () => {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [showSettings, setShowSettings] = useState(false);
  const [showKnowledge, setShowKnowledge] = useState(false);
  const [params, setParams] = useState({
    model: 'deepseek-r1:latest',
    temperature: 0.2,
    max_tokens: 512,
    top_p: 1,
    frequency_penalty: 0,
    presence_penalty: 0,
    stop: ['\n\n'],
    stream: false,
    prompt: '',
    type: 'text' as 'text' | 'image' | 'audio',
  });

  return (
    <React.Fragment>
      <EnhancedChat
        messages={messages}
        setMessages={setMessages}
        params={params}
        setParams={setParams}
        onSettings={() => setShowSettings(true)}
        onKnowledge={() => setShowKnowledge(true)}
      />
    </React.Fragment>
  );
};

export default App;