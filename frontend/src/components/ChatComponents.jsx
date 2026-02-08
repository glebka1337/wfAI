import React, { useRef, useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send, Bot, User, Terminal } from 'lucide-react';
import clsx from 'clsx';
import { useChat } from '../context/ChatContext';
import * as api from '../api/client';

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
    const [input, setInput] = useState('');
    const [commands, setCommands] = useState([]);
    const [showCommands, setShowCommands] = useState(false);
    const textareaRef = useRef(null);

    useEffect(() => {
        loadCommands();
    }, []);

    const loadCommands = async () => {
        try {
            const cmds = await api.fetchCommands();
            setCommands(cmds);
        } catch (e) {
            console.error("Failed to load commands", e);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!input.trim() || isStreaming) return;
        sendMessage(input);
        setInput('');
        setShowCommands(false);

        // Reset height
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault(); // Prevent newline
            handleSubmit(e);
        }
    };

    // Auto-resize & Command Trigger
    const handleInput = (e) => {
        const target = e.target;
        target.style.height = 'auto';
        target.style.height = `${Math.min(target.scrollHeight, 150)}px`;

        const val = target.value;
        setInput(val);

        if (val.startsWith('/')) {
            setShowCommands(true);
        } else {
            setShowCommands(false);
        }
    };

    const handleCommandSelect = (cmd) => {
        setInput(`/${cmd.name} `);
        setShowCommands(false);
        textareaRef.current?.focus();
    };

    const filteredCommands = commands.filter(c =>
        `/${c.name}`.toLowerCase().startsWith(input.split(' ')[0].toLowerCase())
    );

    return (
        <form onSubmit={handleSubmit} className="relative w-full max-w-3xl mx-auto">
            {/* Command Autocomplete Popover */}
            {showCommands && filteredCommands.length > 0 && (
                <div className="absolute bottom-full left-0 mb-2 w-64 bg-slate-800 border border-slate-700 rounded-lg shadow-xl overflow-hidden z-20">
                    <div className="p-2 bg-slate-900 border-b border-slate-800 text-xs text-slate-400 font-semibold uppercase tracking-wider">
                        Available Commands
                    </div>
                    <div className="max-h-48 overflow-y-auto">
                        {filteredCommands.map(cmd => (
                            <button
                                key={cmd.name}
                                type="button"
                                onClick={() => handleCommandSelect(cmd)}
                                className="w-full text-left px-4 py-2 hover:bg-slate-700 flex items-center gap-2 transition-colors"
                            >
                                <Terminal size={14} className="text-indigo-400" />
                                <div>
                                    <div className="text-sm font-medium text-slate-200">/{cmd.name}</div>
                                    <div className="text-xs text-slate-500 truncate">{cmd.description}</div>
                                </div>
                            </button>
                        ))}
                    </div>
                </div>
            )}

            <div className="relative flex items-end gap-2 bg-slate-800/10 backdrop-blur-md border border-slate-700 rounded-3xl p-2 shadow-2xl focus-within:border-indigo-500/50 focus-within:ring-2 focus-within:ring-indigo-500/20 transition-all">
                <textarea
                    ref={textareaRef}
                    rows={1}
                    value={input}
                    onChange={handleInput}
                    onKeyDown={handleKeyDown}
                    placeholder="Message Waifu... (Type '/' for commands)"
                    className="w-full bg-slate-900/50 text-slate-100 placeholder-slate-400 px-4 py-3 rounded-2xl focus:outline-none resize-none max-h-[150px] overflow-y-auto custom-scrollbar border border-transparent focus:border-indigo-500/30 transition-all"
                />

                <button
                    type="submit"
                    disabled={!input.trim() || isStreaming}
                    className="p-3 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed rounded-full text-white transition-all shadow-lg shadow-indigo-600/30 shrink-0 mb-1 mr-1"
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
