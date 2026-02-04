import React, { useEffect, useState } from 'react';
import { X, Terminal, Loader2 } from 'lucide-react';
import * as api from '../api/client';

export default function CommandsModal({ onClose }) {
    const [commands, setCommands] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadCommands();
    }, []);

    const loadCommands = async () => {
        try {
            const data = await api.fetchCommands();
            setCommands(data);
        } catch (e) {
            console.error(e);
            setError("Failed to load commands.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
            <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-2xl shadow-2xl flex flex-col max-h-[80vh]">
                <div className="flex justify-between items-center p-6 border-b border-slate-800">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-indigo-500/10 rounded-lg">
                            <Terminal size={24} className="text-indigo-400" />
                        </div>
                        <h2 className="text-xl font-bold text-slate-100">Available Commands</h2>
                    </div>
                    <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors">
                        <X size={24} />
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto p-6">
                    {isLoading ? (
                        <div className="flex flex-col items-center justify-center py-12 text-slate-500">
                            <Loader2 size={32} className="animate-spin mb-3" />
                            <p>Loading commands...</p>
                        </div>
                    ) : error ? (
                        <div className="text-center py-12 text-red-400 bg-red-900/10 rounded-lg border border-red-900/50">
                            <p>{error}</p>
                            <button onClick={loadCommands} className="mt-2 text-sm underline hover:text-red-300">Try Again</button>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {commands.length === 0 ? (
                                <p className="text-center text-slate-500 py-8">No commands found.</p>
                            ) : (
                                commands.map((cmd) => (
                                    <div key={cmd.name} className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-4 hover:border-indigo-500/30 transition-colors">
                                        <div className="flex items-start justify-between gap-4 mb-2">
                                            <h3 className="font-mono text-indigo-400 font-bold text-lg">
                                                /{cmd.name}
                                            </h3>
                                        </div>
                                        <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap">
                                            {cmd.description}
                                        </p>
                                    </div>
                                ))
                            )}
                        </div>
                    )}
                </div>

                <div className="p-4 border-t border-slate-800 bg-slate-900/50 text-center text-xs text-slate-500">
                    Type these commands in the chat to use them.
                </div>
            </div>
        </div>
    );
}
