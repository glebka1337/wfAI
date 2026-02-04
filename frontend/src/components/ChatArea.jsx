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
            <div className="flex-1 flex flex-col items-center justify-center text-slate-500 bg-slate-950/50 relative">
                {/* Top Bar inside empty state too */}
                <div className="absolute top-4 right-4">
                    <button onClick={onOpenSettings} className="p-2 hover:bg-slate-800 rounded-lg transition-colors">
                        <Settings className="text-slate-400" />
                    </button>
                </div>

                <div className="w-16 h-16 bg-slate-800 rounded-2xl flex items-center justify-center mb-6 shadow-xl shadow-indigo-500/10">
                    <span className="text-3xl">🌸</span>
                </div>
                <h2 className="text-2xl font-bold text-slate-200 mb-2">Welcome to Waifu AI</h2>
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
        <div className="flex-1 flex flex-col h-full bg-slate-950/50 relative">
            {/* Header */}
            <div className="h-16 border-b border-slate-800 flex items-center justify-between px-6 bg-slate-900/50 backdrop-blur-md shrink-0">
                <span className="font-medium text-slate-300">
                    {/* Could show session title here */}
                    Current Session
                </span>
                <button onClick={onOpenSettings} className="p-2 hover:bg-slate-800 rounded-lg transition-colors">
                    <Settings className="text-slate-400" />
                </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-4 py-6 scroll-smooth">
                <div className="max-w-3xl mx-auto min-h-full flex flex-col justify-end">
                    {messages.map((msg, idx) => (
                        <MessageBubble key={idx} message={msg} />
                    ))}
                    {isLoading && (
                        <div className="text-center text-slate-500 py-4 italic animate-pulse">
                            Loading history...
                        </div>
                    )}
                    <div ref={bottomRef} className="h-4" />
                </div>
            </div>

            {/* Input Area */}
            <div className="shrink-0 px-4 pb-6 pt-2 bg-gradient-to-t from-slate-950 to-transparent">
                <ChatInput />
            </div>
        </div>
    );
}
