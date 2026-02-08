import React, { useState } from 'react';
import { MessageSquare, Plus, Trash2, ChevronLeft, ChevronRight, Edit2, Terminal, Image as ImageIcon, Brain } from 'lucide-react';
import { useChat } from '../context/ChatContext';
import EditSessionModal from './EditSessionModal';
import CommandsModal from './CommandsModal';
import WaifuIconsModal from './WaifuIconsModal';
import MemoriesModal from './MemoriesModal';
import clsx from 'clsx';

export default function Sidebar({ isOpen, onToggle }) {
    const { sessions, currentSessionId, setCurrentSessionId, createNewSession, deleteSession, connectionError, loadSessions } = useChat();
    const [editingSession, setEditingSession] = useState(null);
    const [showCommands, setShowCommands] = useState(false);
    const [showIcons, setShowIcons] = useState(false);
    const [showMemories, setShowMemories] = useState(false);

    const handleRename = async (id, newTitle) => {
        try {
            await import('../api/client').then(api => api.updateSession(id, newTitle));
            loadSessions(); // Reload list
        } catch (e) {
            console.error(e);
        }
    };

    if (!isOpen) {
        return (
            <div className="bg-slate-900 border-r border-slate-800 flex flex-col items-center py-4 w-16">
                <button
                    onClick={onToggle}
                    className="p-2 bg-slate-800 rounded-full hover:bg-slate-700 text-slate-400 transition-colors mb-4"
                >
                    <ChevronRight size={20} />
                </button>

                <button
                    onClick={() => createNewSession()}
                    className="p-2 bg-indigo-600 hover:bg-indigo-500 rounded-full transition-colors"
                >
                    <Plus size={20} className="text-white" />
                </button>
            </div>
        );
    }

    return (
        <>
            <div className="w-64 h-full border-r flex flex-col transition-all duration-300 relative bg-white border-zinc-200 dark:bg-slate-900 dark:border-slate-800">
                {/* Header */}
                <div className="p-4 border-b flex items-center justify-between border-zinc-200 dark:border-slate-800">
                    <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
                        Waifu AI
                    </h1>
                    <div className="flex gap-2">
                        <button
                            onClick={() => createNewSession()}
                            className="p-2 bg-indigo-600 hover:bg-indigo-500 rounded-full transition-colors"
                        >
                            <Plus size={16} className="text-white" />
                        </button>
                        <button
                            onClick={onToggle}
                            className="p-2 rounded-full transition-colors text-zinc-500 hover:bg-zinc-100 hover:text-zinc-900 dark:text-slate-400 dark:hover:bg-slate-800"
                        >
                            <ChevronLeft size={16} />
                        </button>
                    </div>
                </div>

                {/* Session List */}
                <div className="flex-1 overflow-y-auto p-2 space-y-2">
                    {sessions.map(session => (
                        <div
                            key={session.uid}
                            onClick={() => setCurrentSessionId(session.uid)}
                            className={clsx(
                                "group flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all duration-200",
                                currentSessionId === session.uid
                                    ? "border-l-4 border-indigo-500 shadow-sm bg-zinc-100 dark:bg-slate-800"
                                    : "text-zinc-600 hover:bg-zinc-50 hover:text-zinc-900 dark:text-slate-400 dark:hover:bg-slate-800/50 dark:hover:text-slate-100"
                            )}
                        >
                            <div className="flex items-center gap-3 overflow-hidden flex-1">
                                <MessageSquare size={18} className={currentSessionId === session.uid ? "text-indigo-400" : "text-zinc-400 dark:text-slate-500"} />
                                <span className={clsx("truncate text-sm font-medium", currentSessionId === session.uid ? "text-zinc-900 dark:text-slate-100" : "")}>
                                    {session.title || "New Chat"}
                                </span>
                            </div>

                            <div className="flex opacity-0 group-hover:opacity-100 transition-opacity">
                                <button
                                    onClick={(e) => { e.stopPropagation(); setEditingSession(session); }}
                                    className="p-1 hover:text-indigo-400 mr-1 text-zinc-400 dark:text-slate-500"
                                >
                                    <Edit2 size={14} />
                                </button>
                                <button
                                    onClick={(e) => { e.stopPropagation(); deleteSession(session.uid); }}
                                    className="p-1 hover:text-red-400 text-zinc-400 dark:text-slate-500"
                                >
                                    <Trash2 size={14} />
                                </button>
                            </div>
                        </div>
                    ))}

                    {sessions.length === 0 && !connectionError && (
                        <div className="text-center text-sm mt-4 text-zinc-400 dark:text-slate-500">
                            No chats yet.
                        </div>
                    )}

                    {connectionError && (
                        <div className="p-3 bg-red-900/20 border border-red-800 rounded-lg mx-2 mt-4 text-center">
                            <p className="text-red-400 text-xs font-semibold mb-2">{connectionError}</p>
                            <button
                                onClick={() => window.location.reload()}
                                className="bg-red-800 hover:bg-red-700 text-white text-xs px-3 py-1 rounded transition-colors"
                            >
                                Retry
                            </button>
                        </div>
                    )}
                </div>

                {/* Footer */}
                <div className="p-4 border-t space-y-2 border-zinc-200 dark:border-slate-800">
                    <button
                        onClick={() => setShowIcons(true)}
                        className="w-full flex items-center justify-center p-2 rounded-md transition-colors bg-zinc-100 hover:bg-zinc-200 text-zinc-600 hover:text-pink-600 dark:bg-slate-800 dark:hover:bg-slate-700 dark:text-slate-400 dark:hover:text-pink-400"
                    >
                        <ImageIcon size={18} className="mr-2" />
                        Waifu Icons
                    </button>
                    <button
                        onClick={() => setShowCommands(true)}
                        className="w-full flex items-center justify-center p-2 rounded-md transition-colors bg-zinc-100 hover:bg-zinc-200 text-zinc-600 hover:text-indigo-600 dark:bg-slate-800 dark:hover:bg-slate-700 dark:text-slate-400 dark:hover:text-indigo-400"
                    >
                        <Terminal size={18} className="mr-2" />
                        Commands
                    </button>
                    <button
                        onClick={() => setShowMemories(true)}
                        className="w-full flex items-center justify-center p-2 rounded-md transition-colors bg-zinc-100 hover:bg-zinc-200 text-zinc-600 hover:text-pink-600 dark:bg-slate-800 dark:hover:bg-slate-700 dark:text-slate-400 dark:hover:text-pink-400"
                    >
                        <Brain size={18} className="mr-2" />
                        Memories
                    </button>
                    <button
                        onClick={onToggle}
                        className="w-full flex items-center justify-center p-2 rounded-md transition-colors bg-zinc-100 hover:bg-zinc-200 text-zinc-600 hover:text-zinc-900 dark:bg-slate-800 dark:hover:bg-slate-700 dark:text-slate-400"
                    >
                        <ChevronLeft size={20} className="mr-2" />
                        Collapse Sidebar
                    </button>
                </div>
            </div>

            {editingSession && (
                <EditSessionModal
                    session={editingSession}
                    onClose={() => setEditingSession(null)}
                    onSave={handleRename}
                />
            )}

            {showCommands && (
                <CommandsModal onClose={() => setShowCommands(false)} />
            )}

            {showIcons && (
                <WaifuIconsModal onClose={() => setShowIcons(false)} />
            )}

            {showMemories && (
                <MemoriesModal onClose={() => setShowMemories(false)} />
            )}
        </>
    );
}
