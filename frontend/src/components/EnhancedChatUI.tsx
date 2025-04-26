import { useState, useRef, useEffect } from "react";
import {
  Send,
  Menu,
  Settings,
  User,
  Bot,
  ArrowLeft,
  Sun,
  Moon,
  Paperclip,
  Languages,
  Brain,
  Compass,
  PaintBucket,
  ChevronDown,
  X, // Added for closing modals
  Upload, // Added for file upload
  Folder, // Added for knowledge stack icon
  Trash2 // Added for deleting knowledge stacks
} from "lucide-react";
import { Message, ModelSettings, sendMessage, uploadKnowledgeFiles } from "../api"; // Adjust the import path as necessary
type ThemeColorType = 'indigo' | 'emerald' | 'rose' | 'amber' | 'blue';

interface DirectionDetectionParams {
  text: string;
}

interface KnowledgeStack {
  id: string;
  name: string;
  files: File[];
}

interface EnhancedChatUIState {
  messages: Message[];
  input: string;
  isLoading: boolean;
  isSidebarOpen: boolean;
  isDarkMode: boolean;
  isRTL: boolean;
  isSettingsOpen: boolean;
  isModelSettingsOpen: boolean;
  isKnowledgeStackOpen: boolean;
  themeColor: ThemeColorType;
  activeModes: string[];
  modelSettings: ModelSettings;
  knowledgeStacks: KnowledgeStack[];
  activeKnowledgeStacks: string[];
  newStackName: string;
  selectedFiles: Record<string, File[]>;
}

export default function EnhancedChatUI() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! I'm Edris. How can I help you today?"
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isRTL, setIsRTL] = useState(false); // Default is LTR now
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isModelSettingsOpen, setIsModelSettingsOpen] = useState(false); // New state for model settings modal
  const [isKnowledgeStackOpen, setIsKnowledgeStackOpen] = useState(false); // New state for knowledge stack modal
  const [themeColor, setThemeColor] = useState<ThemeColorType>("indigo");
  // activeMode is now an array to support multiple active modes
  const [activeModes, setActiveModes] = useState<string[]>([]); // e.g., ["think", "explore"]
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // State for Model Settings
  const [modelSettings, setModelSettings] = useState<ModelSettings>({
    temperature: 0.7,
    top_p: 0.9,
    max_tokens: 150,
    // Add other relevant model parameters here
  });

  // State for Knowledge Stacks
  const [knowledgeStacks, setKnowledgeStacks] = useState<KnowledgeStack[]>([
    // Example structure
    { id: 'default', name: 'Default Knowledge', files: [] },
  ]);
  const [activeKnowledgeStacks, setActiveKnowledgeStacks] = useState(['default']); // IDs of active stacks
  const [newStackName, setNewStackName] = useState('');
  const [selectedFiles, setSelectedFiles] = useState<Record<string, File[]>>({}); // Files selected for upload per stack ID

  // Theme color settings (using Tailwind classes defined in config)
  const themeColors = {
    indigo: {
      primary: "bg-indigo-dark hover:bg-indigo-darker",
      light: "bg-indigo-light",
      text: "text-indigo-text",
      darkText: "text-indigo-darkText",
      border: "border-indigo-DEFAULT", // Using DEFAULT for border if needed
      ring: "ring-indigo-DEFAULT"
    },
    emerald: {
      primary: "bg-emerald-dark hover:bg-emerald-darker",
      light: "bg-emerald-light",
      text: "text-emerald-text",
      darkText: "text-emerald-darkText",
      border: "border-emerald-DEFAULT",
      ring: "ring-emerald-DEFAULT"
    },
    rose: {
      primary: "bg-rose-dark hover:bg-rose-darker",
      light: "bg-rose-light",
      text: "text-rose-text",
      darkText: "text-rose-darkText",
      border: "border-rose-DEFAULT",
      ring: "ring-rose-DEFAULT"
    },
    amber: {
      primary: "bg-amber-dark hover:bg-amber-darker",
      light: "bg-amber-light",
      text: "text-amber-text",
      darkText: "text-amber-darkText",
      border: "border-amber-DEFAULT",
      ring: "ring-amber-DEFAULT"
    },
    blue: {
      primary: "bg-blue-dark hover:bg-blue-darker",
      light: "bg-blue-light",
      text: "text-blue-text",
      darkText: "text-blue-darkText",
      border: "border-blue-DEFAULT",
      ring: "ring-blue-DEFAULT"
    }
  };

  // Current theme color classes
  const currentTheme = themeColors[themeColor];

  // Auto detect text direction
const detectTextDirection = (text: string): boolean => {
    const persianRegex = /[\u0600-\u06FF]/;
    return persianRegex.test(text);
};

  const handleSend = async () => {
    if (input.trim() === "") return;

    const isPersian = detectTextDirection(input);
    if (isPersian !== isRTL) {
      setIsRTL(isPersian);
    }

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);

    try {
      const { response } = await sendMessage({
        prompt: input,
        type: "text",
        history: newMessages,
        modes: activeModes,
        modelSettings: {
          temperature: modelSettings.temperature,
          top_p: modelSettings.top_p,
          max_tokens: modelSettings.max_tokens,
        },
        knowledgeStacks: activeKnowledgeStacks,
      });

      setMessages([...newMessages, { role: "assistant", content: response }]);
    } catch (error) {
      console.error("Error sending message:", error);
      // Add error handling UI feedback here
      setMessages([...newMessages, { 
        role: "assistant", 
        content: "Sorry, I encountered an error. Please try again." 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e:any) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
    // Apply dark class to html element for Tailwind dark mode
    document.documentElement.classList.toggle('dark', !isDarkMode);
  };

  const toggleDirection = () => {
    setIsRTL(!isRTL);
  };

  // Toggle a specific mode (Think or Explore)
  const toggleMode = (mode:any) => {
    setActiveModes(prevModes => {
      if (prevModes.includes(mode)) {
        return prevModes.filter(m => m !== mode);
      } else {
        return [...prevModes, mode];
      }
    });
  };

  // Model Settings Handlers
  const handleModelSettingChange = (setting:any, value:any) => {
    setModelSettings(prevSettings => ({
      ...prevSettings,
      [setting]: value,
    }));
  };

  // Knowledge Stack Handlers
  const handleCreateStack = () => {
    if (newStackName.trim() === '') return;
    const newStack = { id: Date.now().toString(), name: newStackName, files: [] };
    setKnowledgeStacks([...knowledgeStacks, newStack]);
    setActiveKnowledgeStacks([...activeKnowledgeStacks, newStack.id]); // Auto-activate new stack
    setNewStackName('');
  };

  const handleDeleteStack = (stackId:any) => {
      if (stackId === 'default') return; // Prevent deleting default stack
      setKnowledgeStacks(knowledgeStacks.filter(stack => stack.id !== stackId));
      setActiveKnowledgeStacks(activeKnowledgeStacks.filter(id => id !== stackId)); // Deactivate deleted stack
      setSelectedFiles(prevFiles => { // Remove files associated with the deleted stack
          const newFiles = { ...prevFiles };
          delete newFiles[stackId];
          return newFiles;
      });
  };

  interface FileChangeEvent extends React.ChangeEvent<HTMLInputElement> {
    target: HTMLInputElement & {
      files: FileList;
    };
  }

  interface SelectedFilesState {
    [key: string]: File[];
  }

  const handleFileChange = (stackId: string, event: FileChangeEvent): void => {
    const files: File[] = Array.from(event.target.files);
    setSelectedFiles((prevFiles: SelectedFilesState) => ({
      ...prevFiles,
      [stackId]: files
    }));
    // In a real app, you would upload these files to your backend here
    console.log(`Files selected for stack ${stackId}:`, files);
    // You would then likely get a response from the backend confirming upload/vectorization
    // and update the knowledgeStacks state with the file information received from the backend.
  };

  interface StackToggleParams {
    stackId: string;
  }

  const toggleActiveStack = ({ stackId }: StackToggleParams): void => {
    setActiveKnowledgeStacks((prevActive: string[]) => {
      if (prevActive.includes(stackId)) {
        return prevActive.filter((id: string) => id !== stackId);
      } else {
        return [...prevActive, stackId];
      }
    });
  };

  useEffect(() => {
    // Scroll to the latest message
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    // Apply dark mode class to html element on initial load and state change
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

   // Effect to load theme preference from local storage on mount
   useEffect(() => {
    const savedTheme = localStorage.getItem('edris-dark-mode');
    if (savedTheme !== null) {
      setIsDarkMode(JSON.parse(savedTheme));
    }
     const savedThemeColor = localStorage.getItem('edris-theme-color') as ThemeColorType;
     if (savedThemeColor && ['indigo', 'emerald', 'rose', 'amber', 'blue'].includes(savedThemeColor)) {
       setThemeColor(savedThemeColor);
     }
     const savedRTL = localStorage.getItem('edris-rtl');
     if (savedRTL !== null) {
       setIsRTL(JSON.parse(savedRTL));
     }
  }, []);

  // Effect to save theme preference to local storage
  useEffect(() => {
    localStorage.setItem('edris-dark-mode', JSON.stringify(isDarkMode));
    localStorage.setItem('edris-theme-color', themeColor);
    localStorage.setItem('edris-rtl', JSON.stringify(isRTL));
  }, [isDarkMode, themeColor, isRTL]);


  return (
    <div
      className={`flex h-screen ${isDarkMode ? 'bg-gray-900 text-gray-100' : 'bg-gray-50 text-gray-800'} font-sans transition-colors duration-300`}
      // dir is set on the main container based on isRTL state
      dir={isRTL ? "rtl" : "ltr"}
    >
      {/* Sidebar */}
      {/* Added dark:bg-gray-800 and dark:border-gray-700 classes */}
      <div className={`fixed inset-y-0 ${isRTL ? 'right-0' : 'left-0'} transform ${
          isSidebarOpen
            ? 'translate-x-0'
            : isRTL ? 'translate-x-full' : '-translate-x-full'
        } w-72 ${isDarkMode ? 'bg-gray-800' : 'bg-white'} shadow-lg transition-transform duration-300 ease-in-out z-30 md:translate-x-0 md:static
        ${isDarkMode ? 'dark:bg-gray-800' : 'bg-white'} ${isDarkMode ? 'dark:border-gray-700' : 'border-gray-200'} border-r`}> {/* Added border-r */}
        <div className={`p-5 ${isDarkMode ? 'border-gray-700' : 'border-gray-200'} border-b`}>
          <div className="flex items-center justify-between">
            <h2 className={`text-xl font-bold ${isDarkMode ? currentTheme.darkText : currentTheme.text}`}>Edris</h2>
            <button
              className={`p-2 rounded-lg ${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'} md:hidden`}
              onClick={() => setIsSidebarOpen(false)}
            >
              <ArrowLeft size={20} />
            </button>
          </div>
        </div>

        <div className="p-5 flex-1 overflow-y-auto"> {/* Added flex-1 and overflow-y-auto */}
          {/* New Conversation Button - Added Neomorphic style */}
          <button className={`w-full flex items-center justify-center gap-2 ${currentTheme.primary} text-white py-3 px-4 rounded-xl transition duration-200
            shadow-neumorphic-outset hover:shadow-neumorphic-outset-hover active:shadow-neumorphic-inset`}>
            <span>New Conversation</span>
          </button>

          <div className="mt-8">
            <h3 className={`text-sm font-medium ${isDarkMode ? 'text-gray-400' : 'text-gray-500'} mb-3`}>Recent Conversations</h3>
            <div className="space-y-2">
              {[1, 2, 3].map((item) => (
                <button
                  key={item}
                  className={`w-full flex items-center p-3 ${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'} rounded-lg transition text-left`}
                >
                  <div className="flex-1 overflow-hidden">
                    <p className="font-medium truncate">Conversation {item}</p>
                    <p className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-500'} truncate`}>Last message...</p>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar Footer - Added dark:bg-gray-800 and dark:border-gray-700 classes */}
        <div className={`absolute bottom-0 ${isRTL ? 'right-0' : 'left-0'} w-full p-5 ${isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-t`}>
          <div className="space-y-3">
            {/* Theme Toggle - Added Neomorphic style concept (subtle) */}
            <button
              onClick={toggleTheme}
              className={`flex items-center gap-2 p-3 rounded-lg transition w-full text-left
              ${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'}
              ${isDarkMode ? 'dark:hover:bg-gray-700' : 'hover:bg-gray-100'}
              shadow-sm hover:shadow-md active:shadow-inner`} /* Subtle neomorphic effect */
            >
              {isDarkMode ? <Sun size={18} /> : <Moon size={18} />}
              <span>{isDarkMode ? 'Light Mode' : 'Dark Mode'}</span>
            </button>

            {/* Direction Toggle - Added Neomorphic style concept (subtle) */}
            <button
              onClick={toggleDirection}
              className={`flex items-center gap-2 p-3 rounded-lg transition w-full text-left
              ${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'}
              ${isDarkMode ? 'dark:hover:bg-gray-700' : 'hover:bg-gray-100'}
              shadow-sm hover:shadow-md active:shadow-inner`} /* Subtle neomorphic effect */
            >
              <Languages size={18} />
              <span>{isRTL ? 'LTR Mode' : 'RTL Mode'}</span>
            </button>

             {/* Model Settings Button - Added Neomorphic style concept (subtle) */}
             <button
              onClick={() => setIsModelSettingsOpen(true)} // Open model settings modal
              className={`flex items-center gap-2 p-3 rounded-lg transition w-full text-left
              ${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'}
               ${isDarkMode ? 'dark:hover:bg-gray-700' : 'hover:bg-gray-100'}
              shadow-sm hover:shadow-md active:shadow-inner`} /* Subtle neomorphic effect */
            >
              <Settings size={18} />
              <span>Model Settings</span>
            </button>

             {/* Knowledge Stack Button - Added Neomorphic style concept (subtle) */}
             <button
              onClick={() => setIsKnowledgeStackOpen(true)} // Open knowledge stack modal
              className={`flex items-center gap-2 p-3 rounded-lg transition w-full text-left
              ${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'}
               ${isDarkMode ? 'dark:hover:bg-gray-700' : 'hover:bg-gray-100'}
              shadow-sm hover:shadow-md active:shadow-inner`} /* Subtle neomorphic effect */
            >
              <Folder size={18} />
              <span>Knowledge Stacks</span>
            </button>

          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col h-full relative">
        {/* Header - Added dark:bg-gray-800 and dark:border-gray-700 classes */}
        <header className={`${isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} shadow-sm p-4 flex items-center justify-between border-b`}>
          <button
            className={`p-2 rounded-lg ${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'} md:hidden`}
            onClick={() => setIsSidebarOpen(true)}
          >
            <Menu size={20} />
          </button>
          <h1 className="text-lg font-bold text-center flex-1 md:text-right">Edris - AI Assistant</h1>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 md:p-6">
          <div className="max-w-3xl mx-auto space-y-6">
            {messages.map((message, index) => {
              // Detect if message is Persian and should use RTL layout
              const messageIsRTL = detectTextDirection(message.content);

              return (
                <div
                  key={index}
                  className={`flex items-start gap-3 ${
                    message.role === "user" ?
                      (isRTL ? "flex-row-reverse" : "") :
                      (isRTL ? "" : "flex-row-reverse")
                  }`}
                >
                  {/* Avatar - Added Neomorphic style */}
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center shadow-neumorphic-outset
                    ${message.role === "assistant" ?
                      `${currentTheme.light} ${isDarkMode ? currentTheme.darkText : currentTheme.text}` :
                      `${isDarkMode ? 'bg-gray-700' : 'bg-gray-100'} ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`
                    }`}>
                    {message.role === "assistant" ? (
                      <Bot size={20} />
                    ) : (
                      <User size={20} />
                    )}
                  </div>
                  {/* Message Bubble - Added Neomorphic style */}
                  <div
                    className={`p-4 rounded-xl max-w-xl shadow-neumorphic-outset
                      ${message.role === "assistant" ?
                        `${isDarkMode ? 'bg-gray-700 text-white' : `${currentTheme.light}`} ${isRTL ? 'rounded-tr-none' : 'rounded-tl-none'}` :
                        `${isDarkMode ? 'bg-gray-600 text-white' : 'bg-white'} ${isRTL ? 'rounded-tl-none' : 'rounded-tr-none'}`
                      }`}
                    dir={messageIsRTL ? "rtl" : "ltr"} // Set direction based on content
                  >
                    <p className="whitespace-pre-wrap">{message.content}</p>
                  </div>
                </div>
              );
            })}
            {isLoading && (
              <div className={`flex items-start gap-3 ${!isRTL && "flex-row-reverse"}`}>
                 {/* Loading Avatar - Added Neomorphic style */}
                <div className={`w-10 h-10 rounded-full ${isDarkMode ? 'bg-gray-700' : currentTheme.light} ${isDarkMode ? currentTheme.darkText : currentTheme.text} flex items-center justify-center shadow-neumorphic-outset`}>
                  <Bot size={20} />
                </div>
                 {/* Loading Bubble - Added Neomorphic style */}
                <div className={`p-4 rounded-xl ${isDarkMode ? 'bg-gray-700' : currentTheme.light} ${isRTL ? 'rounded-tr-none' : 'rounded-tl-none'} shadow-neumorphic-outset`}>
                  <div className="flex gap-2">
                    <span className={`w-2 h-2 ${isDarkMode ? currentTheme.darkText : currentTheme.text} rounded-full animate-bounce`} style={{ animationDelay: "0ms" }}></span>
                    <span className={`w-2 h-2 ${isDarkMode ? currentTheme.darkText : currentTheme.text} rounded-full animate-bounce`} style={{ animationDelay: "150ms" }}></span>
                    <span className={`w-2 h-2 ${isDarkMode ? currentTheme.darkText : currentTheme.text} rounded-full animate-bounce`} style={{ animationDelay: "300ms" }}></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area - Island Style */}
        {/* Added background, padding, rounded corners, and shadow classes */}
        <div className={`w-full max-w-3xl mx-auto p-4 mb-4 rounded-2xl shadow-island
          ${isDarkMode ? 'bg-gray-800' : 'bg-white'}
          ${isDarkMode ? 'dark:bg-gray-800' : 'bg-white'}`}>
          {/* Action buttons */}
          <div className="flex gap-2 mb-4"> {/* Increased bottom margin */}
            {/* Think Mode Button - Added Neomorphic style */}
            <button
              onClick={() => toggleMode("think")}
              className={`px-3 py-1.5 text-sm rounded-lg flex items-center gap-1 transition
                ${activeModes.includes("think")
                  ? `${currentTheme.primary} text-white shadow-neumorphic-outset active:shadow-neumorphic-inset`
                  : (isDarkMode ? 'bg-gray-700 hover:bg-gray-600 text-white shadow-sm hover:shadow-md active:shadow-inner' : 'bg-gray-100 hover:bg-gray-200 shadow-sm hover:shadow-md active:shadow-inner')
                }`}
            >
              <Brain size={16} />
              <span>Think</span>
            </button>
            {/* Explore Mode Button - Added Neomorphic style */}
            <button
              onClick={() => toggleMode("explore")}
              className={`px-3 py-1.5 text-sm rounded-lg flex items-center gap-1 transition
                ${activeModes.includes("explore")
                  ? `${currentTheme.primary} text-white shadow-neumorphic-outset active:shadow-neumorphic-inset`
                  : (isDarkMode ? 'bg-gray-700 hover:bg-gray-600 text-white shadow-sm hover:shadow-md active:shadow-inner' : 'bg-gray-100 hover:bg-gray-200 shadow-sm hover:shadow-md active:shadow-inner')
                }`}
            >
              <Compass size={16} />
              <span>Explore</span>
            </button>

            {/* Theme color selector - Moved to sidebar footer */}
             {/* Knowledge Stack Selector (Conceptual) */}
             {knowledgeStacks.length > 0 && (
                 <div className="relative ml-auto">
                     <button
                         onClick={() => setIsKnowledgeStackOpen(!isKnowledgeStackOpen)} // Re-use modal toggle for simplicity here
                         className={`px-3 py-1.5 text-sm rounded-lg flex items-center gap-1 transition
                          ${isDarkMode ? 'bg-gray-700 hover:bg-gray-600 text-white' : 'bg-gray-100 hover:bg-gray-200'}
                          shadow-sm hover:shadow-md active:shadow-inner`}
                     >
                         <Folder size={16} />
                         <span>Stacks ({activeKnowledgeStacks.length}/{knowledgeStacks.length})</span>
                         <ChevronDown size={14} />
                     </button>
                      {/* This dropdown could show active stacks and allow toggling,
                          or it could just open the Knowledge Stack modal */}
                     {/* {isKnowledgeStackOpen && (
                         <div className={`absolute bottom-full ${isRTL ? 'right-0' : 'left-0'} mb-2 p-2 rounded-lg shadow-lg ${isDarkMode ? 'bg-gray-700' : 'bg-white'} min-w-max`}>
                             {knowledgeStacks.map(stack => (
                                 <div key={stack.id} className="flex items-center gap-2 text-sm">
                                     <input
                                         type="checkbox"
                                         id={`stack-${stack.id}`}
                                         checked={activeKnowledgeStacks.includes(stack.id)}
                                         onChange={() => toggleActiveStack({ stackId: stack.id })}
                                         className="form-checkbox"
                                     />
                                     <label htmlFor={`stack-${stack.id}`} className={isDarkMode ? 'text-gray-300' : 'text-gray-700'}>{stack.name}</label>
                                 </div>
                             ))}
                         </div>
                     )} */}
                 </div>
             )}

          </div>

          <div className="relative">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message..."
              className={`w-full
                ${isDarkMode ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' : 'bg-gray-50 border-gray-300 placeholder-gray-500'}
                border rounded-xl ${isRTL ? 'pl-24 pr-5' : 'pr-24 pl-5'} py-4
                focus:outline-none focus:${currentTheme.ring} focus:ring-2 focus:border-transparent
                resize-none shadow-neumorphic-inset transition-all duration-200 hover:shadow-neumorphic-inset-active`}
              rows={1}
              style={{ minHeight: "60px", maxHeight: "150px" }}
              dir="auto" // Auto detect direction while typing
            />
            <div className={`absolute ${isRTL ? 'left-3' : 'right-3'} bottom-3 flex gap-2`}>
              {/* File Upload Button - Added Neomorphic style */}
              {/* This button would typically open a file picker, but for simplicity here it's just a button */}
               <button
                 className={`p-2 rounded-lg transition
                   ${isDarkMode ? 'bg-gray-600 hover:bg-gray-500 text-gray-300' : 'bg-gray-200 hover:bg-gray-300 text-gray-600'}
                   shadow-sm hover:shadow-md active:shadow-inner`}
                 onClick={() => alert("File upload functionality needs backend implementation!")} // Placeholder action
               >
                 <Paperclip size={20} />
               </button>
              {/* Send Button - Added Neomorphic style */}
              <button
                onClick={handleSend}
                disabled={input.trim() === "" || isLoading}
                className={`p-2 rounded-lg transition
                  ${input.trim() === "" || isLoading ?
                    (isDarkMode ? 'bg-gray-600 text-gray-400' : 'bg-gray-200 text-gray-400') :
                    `${currentTheme.primary} text-white shadow-neumorphic-outset hover:shadow-neumorphic-outset-hover active:shadow-neumorphic-inset`
                  }`}
              >
                <Send size={20} />
              </button>
            </div>
          </div>
          <p className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-500'} mt-2 text-center`}>
            Edris is an AI assistant and may occasionally make mistakes.
          </p>
        </div>
         {/* Added padding at the bottom to prevent the last message from being hidden by the input island */}
         <div className="pb-24"></div> {/* Adjust padding as needed */}
      </div>

      {/* Model Settings Modal */}
      {/* Added dark mode styles */}
      {isModelSettingsOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className={`p-6 rounded-lg shadow-lg w-full max-w-md
            ${isDarkMode ? 'bg-gray-800 text-gray-100' : 'bg-white text-gray-800'}`}>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">Model Settings</h3>
              <button onClick={() => setIsModelSettingsOpen(false)} className={`p-1 rounded-lg ${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'}`}>
                <X size={20} />
              </button>
            </div>
            <div className="space-y-4">
              {/* Temperature Setting */}
              <div>
                <label htmlFor="temperature" className={`block text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Temperature: {modelSettings.temperature.toFixed(1)}</label>
                <input
                  type="range"
                  id="temperature"
                  min="0"
                  max="2"
                  step="0.1"
                  value={modelSettings.temperature}
                  onChange={(e) => handleModelSettingChange('temperature', parseFloat(e.target.value))}
                  className={`w-full h-2 rounded-lg appearance-none cursor-pointer
                    ${isDarkMode ? 'bg-gray-700' : 'bg-gray-200'} ${currentTheme.primary.replace('bg-', 'accent-')}`} // Use accent color for range slider thumb
                />
                <p className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>Controls randomness. Lowering results in less random completions.</p>
              </div>
              {/* Top P Setting */}
               <div>
                <label htmlFor="top_p" className={`block text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Top P: {modelSettings.top_p.toFixed(1)}</label>
                <input
                  type="range"
                  id="top_p"
                  min="0"
                  max="1"
                  step="0.1"
                  value={modelSettings.top_p}
                  onChange={(e) => handleModelSettingChange('top_p', parseFloat(e.target.value))}
                   className={`w-full h-2 rounded-lg appearance-none cursor-pointer
                    ${isDarkMode ? 'bg-gray-700' : 'bg-gray-200'} ${currentTheme.primary.replace('bg-', 'accent-')}`}
                />
                 <p className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>Controls diversity via nucleus sampling. Higher values consider more tokens.</p>
              </div>
              {/* Max Tokens Setting */}
               <div>
                <label htmlFor="max_tokens" className={`block text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Max Tokens: {modelSettings.max_tokens}</label>
                <input
                  type="range"
                  id="max_tokens"
                  min="50"
                  max="2000" // Adjust max as needed
                  step="50"
                  value={modelSettings.max_tokens}
                  onChange={(e) => handleModelSettingChange('max_tokens', parseInt(e.target.value))}
                   className={`w-full h-2 rounded-lg appearance-none cursor-pointer
                    ${isDarkMode ? 'bg-gray-700' : 'bg-gray-200'} ${currentTheme.primary.replace('bg-', 'accent-')}`}
                />
                 <p className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>The maximum number of tokens to generate in the completion.</p>
              </div>
              {/* Add more model settings as needed */}
            </div>
          </div>
        </div>
      )}

       {/* Knowledge Stack Modal */}
       {/* Added dark mode styles */}
       {isKnowledgeStackOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className={`p-6 rounded-lg shadow-lg w-full max-w-md
            ${isDarkMode ? 'bg-gray-800 text-gray-100' : 'bg-white text-gray-800'}`}>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">Knowledge Stacks</h3>
              <button onClick={() => setIsKnowledgeStackOpen(false)} className={`p-1 rounded-lg ${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'}`}>
                <X size={20} />
              </button>
            </div>
            <div className="space-y-4">
              {/* Create New Stack */}
              <div>
                <label htmlFor="new-stack-name" className={`block text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Create New Stack:</label>
                <div className="flex gap-2 mt-1">
                  <input
                    type="text"
                    id="new-stack-name"
                    value={newStackName}
                    onChange={(e) => setNewStackName(e.target.value)}
                    className={`w-full px-3 py-2 rounded-lg border
                      ${isDarkMode ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' : 'bg-gray-100 border-gray-300 placeholder-gray-500'}
                      focus:outline-none focus:${currentTheme.ring} focus:ring-1`}
                    placeholder="Stack Name"
                  />
                  <button
                    onClick={handleCreateStack}
                    disabled={newStackName.trim() === ''}
                     className={`px-4 py-2 rounded-lg text-white
                      ${newStackName.trim() === '' ?
                        (isDarkMode ? 'bg-gray-600 text-gray-400' : 'bg-gray-300 text-gray-500') :
                        `${currentTheme.primary} shadow-md hover:shadow-lg`
                      } transition`}
                  >
                    Create
                  </button>
                </div>
              </div>

              {/* List of Stacks */}
              <div>
                 <p className={`block text-sm font-medium mb-2 ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Your Stacks:</p>
                 <ul className="space-y-3 max-h-48 overflow-y-auto"> {/* Added max height and overflow */}
                     {knowledgeStacks.map(stack => (
                         <li key={stack.id} className={`p-3 rounded-lg border ${isDarkMode ? 'border-gray-700 bg-gray-700' : 'border-gray-200 bg-gray-50'}`}>
                             <div className="flex items-center justify-between">
                                 <div className="flex items-center gap-2">
                                     <input
                                         type="checkbox"
                                         id={`stack-toggle-${stack.id}`}
                                         checked={activeKnowledgeStacks.includes(stack.id)}
                                         onChange={() => toggleActiveStack({ stackId: stack.id })}
                                         className={`form-checkbox h-4 w-4 ${currentTheme.primary.replace('bg-', 'text-')}`}
                                     />
                                     <label htmlFor={`stack-toggle-${stack.id}`} className={`font-medium ${isDarkMode ? 'text-gray-100' : 'text-gray-800'}`}>{stack.name}</label>
                                 </div>
                                  {stack.id !== 'default' && ( // Prevent deleting default stack
                                     <button onClick={() => handleDeleteStack(stack.id)} className={`p-1 rounded-md ${isDarkMode ? 'hover:bg-gray-600 text-gray-400' : 'hover:bg-gray-200 text-gray-600'} transition`}>
                                         <Trash2 size={16} />
                                     </button>
                                 )}
                             </div>
                              {/* File Upload for Stack */}
                             <div className="mt-3">
                                 <label htmlFor={`file-upload-${stack.id}`} className={`block text-sm font-medium mb-1 ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Upload Files:</label>
                                 <input
                                     type="file"
                                     id={`file-upload-${stack.id}`}
                                     multiple
                                     onChange={(e:any) => handleFileChange(stack.id, e)}
                                     className={`block w-full text-sm file:mr-4 file:py-2 file:px-4
                                         file:rounded-full file:border-0 file:text-sm file:font-semibold
                                         ${isDarkMode ? 'file:bg-gray-600 file:text-gray-100 hover:file:bg-gray-500 text-gray-300' : 'file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 text-gray-700'}
                                         hover:cursor-pointer`}
                                 />
                                 {selectedFiles[stack.id] && selectedFiles[stack.id].length > 0 && (
                                     <p className={`text-xs mt-1 ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                                         Selected: {selectedFiles[stack.id].map(f => f.name).join(', ')}
                                     </p>
                                 )}
                             </div>
                              {/* Display uploaded files (conceptual) */}
                             {/* You would populate this list from the knowledgeStacks state after backend processing */}
                             {/* <div className="mt-3">
                                 <p className={`text-sm font-medium mb-1 ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Files in Stack:</p>
                                 <ul className="text-xs space-y-1">
                                     {stack.files.length === 0 ? (
                                         <li className={isDarkMode ? 'text-gray-400' : 'text-gray-500'}>No files uploaded yet.</li>
                                     ) : (
                                         stack.files.map((file, fileIndex) => (
                                             <li key={fileIndex} className={isDarkMode ? 'text-gray-300' : 'text-gray-700'}>{file.name}</li>
                                         ))
                                     )}
                                 </ul>
                             </div> */}
                         </li>
                     ))}
                 </ul>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
