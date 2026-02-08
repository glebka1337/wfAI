import React, { useRef, useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send, Bot, User, Terminal } from 'lucide-react';
import clsx from 'clsx';
import { useChat } from '../context/ChatContext';
import * as api from '../api/client';

export function MessageBubble({ message, isLast }) {
    const { personaIconUrl, regenerateLastMessage, isStreaming } = useChat();
    const isAi = message.role === 'ai';

    return (
        <div className={clsx(
            "flex w-full mb-6 gap-4 group", // Added group for hover effects
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
                "max-w-[80%] rounded-2xl p-4 shadow-md backdrop-blur-sm relative border",
                isAi
                    ? "bg-white text-slate-800 border-zinc-200 rounded-tl-none dark:bg-slate-800/80 dark:text-slate-100 dark:border-slate-700/50"
                    : "bg-indigo-600 text-white rounded-tr-none shadow-indigo-500/20 border-transparent"
            )}>
                <div className="prose prose-sm leading-relaxed prose-zinc dark:prose-invert">
                    <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>

                {/* Retry Button (Only for last AI message) */}
                {isAi && isLast && !isStreaming && (
                    <div className="absolute -bottom-6 left-0 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                            onClick={() => regenerateLastMessage(false)} // Default to no search? Or use prompt? Maybe add a tiny toggle or just simple retry.
                            className="p-1 rounded cursor-pointer flex items-center gap-1 text-xs bg-zinc-200 text-zinc-600 hover:bg-zinc-300 hover:text-zinc-900 dark:bg-slate-700/50 dark:text-slate-400 dark:hover:text-white dark:hover:bg-slate-600"
                            title="Regenerate response"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M21.5 2v6h-6"></path>
                                <path d="M21.34 15.57a10 10 0 1 1-.57-8.38"></path>
                            </svg>
                            Try Again
                        </button>
                    </div>
                )}
            </div>

            {/* Avatar for User */}
            {!isAi && (
                <div className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 bg-zinc-300 dark:bg-slate-700">
                    <User size={16} className="text-slate-600 dark:text-slate-300" />
                </div>
            )}
        </div>
    );
}

export function ChatInput() {
    const { sendMessage, isStreaming, currentSessionId } = useChat();
    const [input, setInput] = useState('');
    const [useSearch, setUseSearch] = useState(false);
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
        if (e) e.preventDefault();
        if (!input.trim() || isStreaming) return;

        sendMessage(input, useSearch);
        setInput('');
        setUseSearch(false);
        setShowCommands(false);

        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

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
        <form onSubmit={handleSubmit} className="relative w-full max-w-3xl mx-auto group">
            {/* Command Autocomplete Popover */}
            {showCommands && filteredCommands.length > 0 && (
                <div className="absolute bottom-full left-0 mb-2 w-64 rounded-lg shadow-xl overflow-hidden z-20 bg-white border border-zinc-200 dark:bg-slate-800 dark:border-slate-700">
                    <div className="p-2 border-b text-xs font-semibold uppercase tracking-wider bg-zinc-50 border-zinc-200 text-zinc-500 dark:bg-slate-900 dark:border-slate-800 dark:text-slate-400">
                        Available Commands
                    </div>
                    <div className="max-h-48 overflow-y-auto">
                        {filteredCommands.map(cmd => (
                            <button
                                key={cmd.name}
                                type="button"
                                onClick={() => handleCommandSelect(cmd)}
                                className="w-full text-left px-4 py-2 flex items-center gap-2 transition-colors hover:bg-zinc-100 dark:hover:bg-slate-700"
                            >
                                <Terminal size={14} className="text-indigo-600 dark:text-indigo-400" />
                                <div>
                                    <div className="text-sm font-medium text-zinc-800 dark:text-slate-200">/{cmd.name}</div>
                                    <div className="text-xs text-zinc-500 truncate dark:text-slate-500">{cmd.description}</div>
                                </div>
                            </button>
                        ))}
                    </div>
                </div>
            )}

            <div className="relative flex items-end gap-2 backdrop-blur-md border rounded-3xl p-2 shadow-2xl transition-all bg-white border-zinc-200 focus-within:border-indigo-400 focus-within:ring-2 focus-within:ring-indigo-400/20 dark:bg-slate-800/10 dark:border-slate-700 dark:focus-within:border-indigo-500/50 dark:focus-within:ring-indigo-500/20">
                <textarea
                    ref={textareaRef}
                    rows={1}
                    value={input}
                    onChange={handleInput}
                    onKeyDown={handleKeyDown}
                    placeholder={`Message Waifu...${useSearch ? ' (Web Search ON)' : ''}`}
                    className="w-full px-4 py-3 rounded-2xl focus:outline-none resize-none max-h-[150px] overflow-y-auto custom-scrollbar border border-transparent transition-all bg-zinc-50 text-zinc-900 placeholder-zinc-400 focus:border-indigo-400/30 dark:bg-slate-900/50 dark:text-slate-100 dark:placeholder-slate-400 dark:focus:border-indigo-500/30"
                />

                {/* Search Toggle */}
                <button
                    type="button"
                    onClick={() => setUseSearch(!useSearch)}
                    className={clsx(
                        "p-3 rounded-full transition-all shrink-0 mb-1",
                        useSearch
                            ? "bg-sky-100 text-sky-600 hover:bg-sky-200 dark:bg-sky-500/20 dark:text-sky-400 dark:hover:bg-sky-500/30"
                            : "text-zinc-400 hover:text-zinc-600 hover:bg-zinc-100 dark:text-slate-500 dark:hover:text-slate-300 dark:hover:bg-slate-800"
                    )}
                    title="Toggle Web Search"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                </button>

                <button
                    type="submit"
                    disabled={!input.trim() || isStreaming}
                    className={clsx(
                        "p-3 rounded-full text-white transition-all shadow-lg shrink-0 mb-1 mr-1",
                        useSearch
                            ? "bg-sky-500 hover:bg-sky-600 shadow-sky-500/30 dark:bg-sky-600 dark:hover:bg-sky-500 dark:shadow-sky-600/30"
                            : "bg-indigo-500 hover:bg-indigo-600 shadow-indigo-500/30 dark:bg-indigo-600 dark:hover:bg-indigo-500 dark:shadow-indigo-600/30",
                        (!input.trim() || isStreaming) && "opacity-50 cursor-not-allowed"
                    )}
                >
                    <Send size={18} />
                </button>
            </div>

            <div className="text-center mt-2 text-xs text-zinc-400 dark:text-slate-500">
                AI can make mistakes. Check important info.
            </div>
        </form>
    );
}
