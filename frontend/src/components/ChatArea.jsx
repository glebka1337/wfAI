import React, { useRef, useEffect } from 'react';
import { useChat } from '../context/ChatContext';
import { MessageBubble, ChatInput } from './ChatComponents';
import { Settings } from 'lucide-react';

export default function ChatArea({ onOpenSettings }) {
    const { messages, currentSessionId, isLoading } = useChat();
    const bottomRef = useRef(null);

    // Auto-scroll to bottom
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    if (!currentSessionId && messages.length === 0) {
        return (
            <div className="flex-1 flex flex-col items-center justify-center relative bg-zinc-50 text-zinc-500 dark:bg-slate-950/50 dark:text-slate-500">
                {/* Top Bar inside empty state too */}
                <div className="absolute top-4 right-4">
                    <button onClick={onOpenSettings} className="p-2 rounded-lg transition-colors hover:bg-zinc-200 dark:hover:bg-slate-800">
                        <Settings className="text-zinc-500 dark:text-slate-400" />
                    </button>
                </div>

                <div className="w-16 h-16 rounded-2xl flex items-center justify-center mb-6 shadow-xl shadow-indigo-500/10 bg-white dark:bg-slate-800">
                    <span className="text-3xl">🌸</span>
                </div>
                <h2 className="text-2xl font-bold mb-2 text-zinc-800 dark:text-slate-200">Welcome to Waifu AI</h2>
                <p className="max-w-md text-center mb-8">
                    Your personal AI assistant with memory and personality.
                    Start a new chat to begin.
                </p>
                <div className="w-full max-w-2xl px-4">
                    <ChatInput />
                </div>
            </div>
        );
    }

    return (
        <div className="flex-1 flex flex-col h-full relative bg-zinc-50 dark:bg-slate-950/50">
            {/* Header */}
            <div className="h-16 border-b flex items-center justify-between px-6 backdrop-blur-md shrink-0 bg-white/50 border-zinc-200 dark:bg-slate-900/50 dark:border-slate-800">
                <span className="font-medium text-zinc-700 dark:text-slate-300">
                    {/* Could show session title here */}
                    Current Session
                </span>
                <button onClick={onOpenSettings} className="p-2 rounded-lg transition-colors hover:bg-zinc-200 dark:hover:bg-slate-800">
                    <Settings className="text-zinc-500 dark:text-slate-400" />
                </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-4 py-6 scroll-smooth">
                <div className="max-w-3xl mx-auto min-h-full flex flex-col justify-end">
                    {messages.map((msg, idx) => (
                        <MessageBubble
                            key={idx}
                            message={msg}
                            isLast={idx === messages.length - 1}
                        />
                    ))}
                    {isLoading && (
                        <div className="text-center py-4 italic animate-pulse text-slate-500">
                            Loading history...
                        </div>
                    )}
                    <div ref={bottomRef} className="h-4" />
                </div>
            </div>

            {/* Input Area */}
            <div className="shrink-0 px-4 pb-6 pt-2 bg-gradient-to-t from-zinc-50 dark:from-slate-950 to-transparent">
                <ChatInput />
            </div>
        </div>
    );
}
