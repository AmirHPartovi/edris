/* src/components/KnowledgeModal.tsx */
import React, { useCallback, useState } from 'react';
import { Dialog } from '@headlessui/react';
import { useDropzone } from 'react-dropzone';

interface Props { onClose: () => void; }
export default function KnowledgeModal({ onClose }: Props) {
  const [files, setFiles] = useState<File[]>([]);
  const onDrop = useCallback((accepted: File[]) => setFiles(accepted), []);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const upload = () => {
    // call backend endpoint to ingest files into knowledge stack
    const form = new FormData();
    files.forEach(f => form.append('files', f));
    fetch(`${import.meta.env.VITE_SERVER_URL}/knowledge/upload`, { method: 'POST', body: form });
    onClose();
  };

  return (
    <Dialog open onClose={onClose} className="fixed inset-0 z-10 flex items-center justify-center">
      <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg z-20 w-96">
        <Dialog.Title className="text-xl mb-4">Knowledge Stack</Dialog.Title>
        <div {...getRootProps()} className="border-dashed border-2 p-4 text-center cursor-pointer">
          <input {...getInputProps()} />
          {isDragActive ? <p>Drop files here ...</p> : <p>Drag & drop files, or click to select</p>}
        </div>
        <ul className="mt-4 max-h-40 overflow-auto">
          {files.map(f => <li key={f.name}>{f.name}</li>)}
        </ul>
        <button onClick={upload} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded">Upload</button>
      </div>
    </Dialog>
  );
}