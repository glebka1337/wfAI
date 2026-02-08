import React, { useEffect, useState } from 'react';
import { X, Brain, Loader2, Trash2 } from 'lucide-react';
import * as api from '../api/client';

export default function MemoriesModal({ onClose }) {
    const [memories, setMemories] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadMemories();
    }, []);

    const loadMemories = async () => {
        try {
            const data = await api.fetchMemories();
            setMemories(data);
        } catch (e) {
            console.error(e);
            setError("Failed to load memories.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleDelete = async (vectorId) => {
        if (!confirm('Are you sure you want to delete this memory?')) return;
        try {
            await api.deleteMemory(vectorId);
            setMemories(memories.filter(m => m.vector_id !== vectorId));
        } catch (e) {
            console.error(e);
            alert("Failed to delete memory");
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
            <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-3xl shadow-2xl flex flex-col max-h-[85vh]">
                <div className="flex justify-between items-center p-6 border-b border-slate-800">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-pink-500/10 rounded-lg">
                            <Brain size={24} className="text-pink-400" />
                        </div>
                        <h2 className="text-xl font-bold text-slate-100">Long-Term Memories</h2>
                    </div>
                    <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors">
                        <X size={24} />
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto p-6">
                    {isLoading ? (
                        <div className="flex flex-col items-center justify-center py-12 text-slate-500">
                            <Loader2 size={32} className="animate-spin mb-3" />
                            <p>Loading memories...</p>
                        </div>
                    ) : error ? (
                        <div className="text-center py-12 text-red-400 bg-red-900/10 rounded-lg border border-red-900/50">
                            <p>{error}</p>
                            <button onClick={loadMemories} className="mt-2 text-sm underline hover:text-red-300">Try Again</button>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {memories.length === 0 ? (
                                <p className="text-center text-slate-500 py-8">No memories found.</p>
                            ) : (
                                memories.map((mem) => (
                                    <div key={mem.vector_id} className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-4 hover:border-pink-500/30 transition-colors flex justify-between gap-4 group">
                                        <div className="flex-1">
                                            <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap">
                                                {mem.content}
                                            </p>
                                            <div className="flex gap-2 mt-2">
                                                <span className="text-xs bg-slate-800 text-slate-500 px-2 py-0.5 rounded border border-slate-700">
                                                    Score: {mem.importance.toFixed(2)}
                                                </span>
                                                <span className="text-xs text-slate-600 px-2 py-0.5">
                                                    {new Date(mem.created_at).toLocaleString()}
                                                </span>
                                            </div>
                                        </div>
                                        <button
                                            onClick={() => handleDelete(mem.vector_id)}
                                            className="text-slate-600 hover:text-red-400 self-start opacity-0 group-hover:opacity-100 transition-opacity p-2"
                                            title="Delete Memory"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                ))
                            )}
                        </div>
                    )}
                </div>

                <div className="p-4 border-t border-slate-800 bg-slate-900/50 text-center text-xs text-slate-500">
                    Memories are automatically created from your conversations.
                </div>
            </div>
        </div>
    );
}
