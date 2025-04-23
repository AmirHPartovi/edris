/* src/components/MessageInput.tsx */
import React, { useState } from 'react';
import { sendMessage, ChatParams } from '../api';

interface Props {
  onSend: (msg: string) => void;
  onResponse: (resp: string) => void;
  params: ChatParams;
}

export default function MessageInput({ onSend, onResponse, params }: Props) {
  const [text, setText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSend = async () => {
    if (!text.trim() || isLoading) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      onSend(text);
      const resp = await sendMessage({ ...params, prompt: text });
      onResponse(resp);
      setText('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-4 bg-white dark:bg-gray-900 border-t">
      {error && (
        <div className="mb-2 text-red-500 text-sm">{error}</div>
      )}
      <div className="flex">
        <textarea
          className="flex-1 resize-none p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700"
          rows={2}
          value={text}
          onChange={e => setText(e.target.value)}
          disabled={isLoading}
          placeholder="Type your message..."
        />
        <button
          onClick={handleSend}
          disabled={isLoading || !text.trim()}
          className={`ml-2 px-4 py-2 rounded text-white ${
            isLoading || !text.trim()
              ? 'bg-blue-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
}