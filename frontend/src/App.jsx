import React, { useState, useEffect } from 'react';
import { ChatProvider, useChat } from './context/ChatContext';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import SettingsModal from './components/SettingsModal';

function Layout() {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const { currentSessionId, sessions } = useChat();

  // --- Theme Logic ---
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'dark');

  useEffect(() => {
    const root = window.document.documentElement;
    console.log('🎨 Theme changed to:', theme);
    console.log('🎨 Root element classes before:', root.className);

    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }

    console.log('🎨 Root element classes after:', root.className);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    console.log('🎨 toggleTheme called! Current theme:', theme);
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };
  // -------------------

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
    <div className="flex w-full h-full overflow-hidden font-sans selection:bg-indigo-500/30 transition-colors duration-300 bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
      <Sidebar isOpen={isSidebarOpen} onToggle={() => setIsSidebarOpen(!isSidebarOpen)} />

      <main className="flex-1 flex flex-col min-w-0 relative transition-all duration-300 bg-zinc-100 dark:bg-slate-950/50">
        <ChatArea onOpenSettings={() => setIsSettingsOpen(true)} />
      </main>

      {isSettingsOpen && (
        <SettingsModal
          onClose={() => setIsSettingsOpen(false)}
          theme={theme}
          toggleTheme={toggleTheme}
        />
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
