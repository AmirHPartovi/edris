/* src/components/MessageList.tsx */
import React from 'react';

interface Props { messages: { role: string; content: string }[]; }
export default function MessageList({ messages }: Props) {
  return (
    <div className="flex-1 overflow-auto p-4 space-y-4 bg-gray-100 dark:bg-gray-800">
      {messages.map((m, i) => (
        <div key={i} className={`max-w-xl ${m.role==='user'?'self-end bg-blue-500 text-white':'self-start bg-white dark:bg-gray-700 text-gray-900 p-3 rounded-lg'}`}>
          {m.content}
        </div>
      ))}
    </div>
  );
}