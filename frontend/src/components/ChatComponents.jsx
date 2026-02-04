import React, { useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send, Bot, User } from 'lucide-react';
import clsx from 'clsx';
import { useChat } from '../context/ChatContext';

export function MessageBubble({ message }) {
    const { personaIconUrl } = useChat();
    const isAi = message.role === 'ai';

    return (
        <div className={clsx(
            "flex w-full mb-6 gap-4",
            isAi ? "justify-start" : "justify-end"
        )}>
            {/* Avatar for AI */}
            {isAi && (
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shrink-0 shadow-lg shadow-indigo-500/20 overflow-hidden">
                    {personaIconUrl ? (
                        <img src={personaIconUrl} alt="Waifu" className="w-full h-full object-cover" />
                    ) : (
                        <Bot size={16} className="text-white" />
                    )}
                </div>
            )}

            <div className={clsx(
                "max-w-[80%] rounded-2xl p-4 shadow-md backdrop-blur-sm",
                isAi
                    ? "bg-slate-800/80 text-slate-100 rounded-tl-none border border-slate-700/50"
                    : "bg-indigo-600 text-white rounded-tr-none shadow-indigo-500/20"
            )}>
                <div className="prose prose-invert prose-sm leading-relaxed">
                    <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>
            </div>

            {/* Avatar for User */}
            {!isAi && (
                <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center shrink-0">
                    <User size={16} className="text-slate-300" />
                </div>
            )}
        </div>
    );
}

export function ChatInput() {
    const { sendMessage, isStreaming } = useChat();
    const [input, setInput] = React.useState('');
    const textareaRef = useRef(null);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!input.trim() || isStreaming) return;
        sendMessage(input);
        setInput('');

        // Reset height
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            handleSubmit(e);
        }
    };

    // Auto-resize
    const handleInput = (e) => {
        const target = e.target;
        target.style.height = 'auto';
        target.style.height = `${Math.min(target.scrollHeight, 150)}px`;
        setInput(target.value);
    };

    return (
        <form onSubmit={handleSubmit} className="relative w-full max-w-3xl mx-auto">
            <div className="relative flex items-end gap-2 bg-slate-800/50 backdrop-blur-md border border-slate-700 rounded-3xl p-2 shadow-2xl focus-within:border-indigo-500/50 focus-within:ring-2 focus-within:ring-indigo-500/20 transition-all">
                <textarea
                    ref={textareaRef}
                    rows={1}
                    value={input}
                    onChange={handleInput}
                    onKeyDown={handleKeyDown}
                    placeholder="Message Waifu..."
                    className="w-full bg-transparent text-slate-100 placeholder-slate-400 px-4 py-3 focus:outline-none resize-none max-h-[150px] overflow-y-auto custom-scrollbar"
                />

                <button
                    type="submit"
                    disabled={!input.trim() || isStreaming}
                    className="p-3 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed rounded-full text-white transition-all shadow-lg shadow-indigo-600/30"
                >
                    <Send size={18} />
                </button>
            </div>

            <div className="text-center mt-2 text-xs text-slate-500">
                AI can make mistakes. Check important info.
            </div>
        </form>
    );
}
