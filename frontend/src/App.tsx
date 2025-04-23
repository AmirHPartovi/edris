import React, { useState } from 'react';
import ChatHeader from './components/ChatHeader';
import MessageList from './components/MessageList';
import MessageInput from './components/MessageInput';
import SettingsModal from './components/SettingsModal';
import KnowledgeModal from './components/KnowledgeModal';

interface Props {
  onSettings: () => void;
  onKnowledge: () => void;
}

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
    type: 'text' as const,
  });

  return (
    <div className="flex h-full">
      {/* Sidebar */}
      <aside className="w-64 bg-white dark:bg-gray-900 border-r p-4 hidden md:block">
        <button
          className="w-full mb-4 p-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          onClick={() => setShowKnowledge(true)}
        >
          Manage Knowledge Stack
        </button>
        <button
          className="w-full p-2 bg-green-600 text-white rounded hover:bg-green-700"
          onClick={() => setShowSettings(true)}
        >
          Model Settings
        </button>
      </aside>

      {/* Main Chat Area */}
      <div className="flex flex-col flex-1">
        <ChatHeader onSettings={() => setShowSettings(true)} onKnowledge={() => setShowKnowledge(true)} />
        <MessageList messages={messages} />
        <MessageInput
          onSend={msg => setMessages(prev => [...prev, { role: 'user', content: msg }])}
          onResponse={resp => setMessages(prev => [...prev, { role: 'assistant', content: resp }])}
          params={params}
        />
      </div>

      {/* Modals */}
      {showSettings && (
        <SettingsModal
          params={params}
          onChange={setParams}
          onClose={() => setShowSettings(false)}
        />
      )}
      {showKnowledge && <KnowledgeModal onClose={() => setShowKnowledge(false)} />}
    </div>
  );
};

export default App;