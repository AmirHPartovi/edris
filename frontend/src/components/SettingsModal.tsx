/* src/components/SettingsModal.tsx */
import React from 'react';
import { Dialog } from '@headlessui/react';

interface Props { params: any; onChange: any; onClose: () => void; }
export default function SettingsModal({ params, onChange, onClose }: Props) {
  const keys = ['model','temperature','max_tokens','top_p','frequency_penalty','presence_penalty','stream'];
  return (
    <Dialog open onClose={onClose} className="fixed inset-0 z-10 flex items-center justify-center">
      <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg z-20 w-80 space-y-4">
        <Dialog.Title className="text-xl">Model Settings</Dialog.Title>
        {keys.map(k => (
          <div key={k} className="flex justify-between items-center">
            <label className="capitalize mr-2">{k}</label>
            {typeof params[k] === 'boolean' ? (
              <input 
                type="checkbox" 
                checked={params[k]} 
                onChange={e => onChange({ ...params, [k]: e.target.checked })}
                title={`Toggle ${k}`}
                aria-label={`Toggle ${k}`}
              />
            ) : typeof params[k] === 'number' ? (
              <input
                type="number"
                value={params[k]}
                onChange={e => onChange({ ...params, [k]: parseFloat(e.target.value) })}
                className="w-20 p-1 border rounded dark:bg-gray-700"
                title={`Enter ${k} value`}
                placeholder={`Enter ${k}`}
              />
            ) : (
              <input
                type="text"
                value={params[k]}
                onChange={e => onChange({ ...params, [k]: e.target.value })}
                className="w-32 p-1 border rounded dark:bg-gray-700"
                title={`Enter ${k} value`}
                placeholder={`Enter ${k}`}
              />
            )}
          </div>
        ))}
        <button onClick={onClose} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded">Close</button>
      </div>
    </Dialog>
  );
}
