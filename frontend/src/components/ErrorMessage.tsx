import { X } from 'lucide-react';
interface ErrorMessageProps {
  message: string;
  onClose: () => void;
}
const onClose = () => {
    // Handle close action
    console.log("Error message closed");
}
export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onClose }) => {
  return (
    <div className="fixed bottom-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg flex items-center gap-2">
      <span>{message}</span>
        <button onClick={onClose} className="hover:text-red-200">
        <X size={16} />
      </button>
    </div>
  );
};