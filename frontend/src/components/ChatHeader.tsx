/* src/components/ChatHeader.tsx */
import React from 'react';
import { Settings } from 'lucide-react';

interface Props { onSettings: () => void; }
export default function ChatHeader({ onSettings }: Props) {
  return (
    <div className="flex items-center justify-between px-4 py-2 bg-white dark:bg-gray-900 border-b">
      <h1 className="text-lg font-semibold">Edris</h1>
      <button
        onClick={onSettings}
        className="p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700"
        aria-label="Open settings"
        title="Open settings"
      >
        <Settings className="w-5 h-5" />
      </button>
    </div>
  );
}