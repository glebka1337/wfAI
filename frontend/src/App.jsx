import React, { useState, useEffect } from 'react';
import { ChatProvider, useChat } from './context/ChatContext';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import SettingsModal from './components/SettingsModal';

function Layout() {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const { currentSessionId, sessions } = useChat();

  // Dynamic Title
  useEffect(() => {
    if (currentSessionId) {
      const session = sessions.find(s => s.uid === currentSessionId);
      document.title = session?.title || "Waifu AI";
    } else {
      document.title = "Waifu AI";
    }
  }, [currentSessionId, sessions]);

  return (
    <div className="flex w-full h-full bg-slate-950 text-slate-100 overflow-hidden font-sans selection:bg-indigo-500/30">
      <Sidebar isOpen={isSidebarOpen} onToggle={() => setIsSidebarOpen(!isSidebarOpen)} />

      <main className="flex-1 flex flex-col min-w-0 relative transition-all duration-300">
        <ChatArea onOpenSettings={() => setIsSettingsOpen(true)} />
      </main>

      {isSettingsOpen && (
        <SettingsModal onClose={() => setIsSettingsOpen(false)} />
      )}
    </div>
  );
}

export default function App() {
  return (
    <ChatProvider>
      <Layout />
    </ChatProvider>
  );
}
