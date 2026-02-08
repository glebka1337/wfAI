import React, { useState, useEffect } from 'react';
import { X, User, Sparkles, Save } from 'lucide-react';
import clsx from 'clsx';
import * as api from '../api/client';

export default function SettingsModal({ onClose, theme, toggleTheme }) {
    const [activeTab, setActiveTab] = useState('user'); // 'user' | 'waifu'
    const [userData, setUserData] = useState({ username: '', bio: '' });
    const [waifuData, setWaifuData] = useState({ name: '', system_instruction: '', traits: {}, icon_url: null, language: 'English' });
    const [loading, setLoading] = useState(false);
    const [msg, setMsg] = useState({ type: '', text: '' });

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const [u, w] = await Promise.all([
                api.fetchUserProfile(),
                api.fetchWaifuPersona()
            ]);
            setUserData(u);
            setWaifuData(w);
        } catch (e) {
            console.error(e);
            setMsg({ type: 'error', text: 'Failed to load settings' });
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        setLoading(true);
        setMsg(null);
        try {
            if (activeTab === 'user') {
                await api.updateUserProfile(userData);
            } else {
                await api.updateWaifuPersona(waifuData);
            }
            setMsg({ type: 'success', text: 'Saved successfully!' });
        } catch (e) {
            setMsg({ type: 'error', text: 'Failed to save' });
        } finally {
            setLoading(false);
        }
    };

    // Helper for traits (JSON object)
    const handleTraitChange = (key, val) => {
        setWaifuData(prev => ({
            ...prev,
            traits: { ...prev.traits, [key]: parseFloat(val) }
        }));
    };

    // Theme logic moved to App.jsx

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 text-slate-100">
            <div className="w-full max-w-2xl rounded-2xl shadow-2xl flex flex-col overflow-hidden max-h-[85vh] bg-white border border-zinc-200 dark:bg-slate-900 dark:border-slate-800">

                {/* Header */}
                <div className="flex items-center justify-between p-6 border-b bg-white border-zinc-200 dark:bg-slate-900 dark:border-slate-800">
                    <h2 className="text-xl font-bold text-zinc-900 dark:text-white">Settings</h2>
                    <div className="flex gap-2">
                        <button
                            onClick={toggleTheme}
                            className="p-2 rounded-lg transition-colors text-zinc-500 hover:bg-zinc-100 dark:text-slate-400 dark:hover:bg-slate-800 hover:text-yellow-400"
                            title="Toggle Theme"
                        >
                            {theme === 'dark' ? '🌙' : '☀️'}
                        </button>
                        <button onClick={onClose} className="text-zinc-500 hover:text-zinc-900 dark:text-slate-400 dark:hover:text-white">
                            <X size={24} />
                        </button>
                    </div>
                </div>

                {/* Tabs */}
                <div className="flex border-b bg-zinc-50 border-zinc-200 dark:bg-slate-900/50 dark:border-slate-800">
                    <button
                        onClick={() => setActiveTab('user')}
                        className={clsx(
                            "flex-1 py-4 flex items-center justify-center gap-2 text-sm font-medium transition-colors",
                            activeTab === 'user'
                                ? "border-b-2 border-indigo-500 bg-white text-indigo-600 dark:bg-slate-800/50 dark:text-indigo-400"
                                : "text-zinc-500 hover:text-zinc-900 dark:text-slate-400 dark:hover:text-slate-200"
                        )}
                    >
                        <User size={18} /> User Profile
                    </button>
                    <button
                        onClick={() => setActiveTab('waifu')}
                        className={clsx(
                            "flex-1 py-4 flex items-center justify-center gap-2 text-sm font-medium transition-colors",
                            activeTab === 'waifu'
                                ? "border-b-2 border-purple-500 bg-white text-purple-600 dark:bg-slate-800/50 dark:text-purple-400"
                                : "text-zinc-500 hover:text-zinc-900 dark:text-slate-400 dark:hover:text-slate-200"
                        )}
                    >
                        <Sparkles size={18} /> Waifu Persona
                    </button>
                </div>

                {/* Content */}
                <div className="p-6 overflow-y-auto flex-1 bg-white dark:bg-slate-900">
                    {msg && (
                        <div className={clsx("mb-4 p-3 rounded text-sm", msg.type === 'error' ? "bg-red-900/30 text-red-200" : "bg-green-900/30 text-green-200")}>
                            {msg.text}
                        </div>
                    )}

                    {activeTab === 'user' ? (
                        <div className="space-y-4">
                            <label className="block">
                                <span className="text-sm text-zinc-500 dark:text-slate-400">Username</span>
                                <input
                                    type="text"
                                    value={userData.username}
                                    onChange={e => setUserData({ ...userData, username: e.target.value })}
                                    className="mt-1 w-full rounded-lg p-3 focus:outline-none focus:border-indigo-500 dark:focus:border-indigo-500 bg-zinc-50 border border-zinc-200 text-zinc-900 dark:bg-slate-800 dark:border-slate-700 dark:text-white"
                                />
                            </label>
                            <label className="block">
                                <span className="text-sm text-zinc-500 dark:text-slate-400">Bio</span>
                                <textarea
                                    rows={3}
                                    value={userData.bio}
                                    onChange={e => setUserData({ ...userData, bio: e.target.value })}
                                    className="mt-1 w-full rounded-lg p-3 focus:outline-none focus:border-indigo-500 dark:focus:border-indigo-500 bg-zinc-50 border border-zinc-200 text-zinc-900 dark:bg-slate-800 dark:border-slate-700 dark:text-white"
                                />
                            </label>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <label className="block">
                                    <span className="text-sm text-zinc-500 dark:text-slate-400">Name</span>
                                    <input
                                        type="text"
                                        value={waifuData.name}
                                        onChange={e => setWaifuData({ ...waifuData, name: e.target.value })}
                                        className="mt-1 w-full rounded-lg p-3 focus:outline-none focus:border-purple-500 dark:focus:border-purple-500 bg-zinc-50 border border-zinc-200 text-zinc-900 dark:bg-slate-800 dark:border-slate-700 dark:text-white"
                                    />
                                </label>
                                <label className="block">
                                    <span className="text-sm text-zinc-500 dark:text-slate-400">Language / Язык</span>
                                    <select
                                        value={waifuData.language || 'English'}
                                        onChange={e => setWaifuData({ ...waifuData, language: e.target.value })}
                                        className="mt-1 w-full rounded-lg p-3 focus:outline-none focus:border-purple-500 cursor-pointer bg-zinc-50 border border-zinc-200 text-zinc-900 dark:bg-slate-800 dark:border-slate-700 dark:text-white"
                                    >
                                        <option value="English">English</option>
                                        <option value="Russian">Russian (Русский)</option>
                                    </select>
                                </label>
                            </div>

                            <label className="block">
                                <span className="text-sm text-zinc-500 dark:text-slate-400">System Instruction</span>
                                <textarea
                                    rows={5}
                                    value={waifuData.system_instruction}
                                    onChange={e => setWaifuData({ ...waifuData, system_instruction: e.target.value })}
                                    className="mt-1 w-full rounded-lg p-3 focus:outline-none focus:border-purple-500 font-mono text-sm bg-zinc-50 border border-zinc-200 text-zinc-900 dark:bg-slate-800 dark:border-slate-700 dark:text-white"
                                />
                            </label>

                            {/* Traits Demo */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                {[
                                    { key: 'warmth', label: 'Warmth', desc: 'Affectionate vs Cold' },
                                    { key: 'chaos', label: 'Chaos', desc: 'Predictable vs Random' },
                                    { key: 'empathy', label: 'Empathy', desc: 'Understanding vs Indifferent' },
                                    { key: 'sarcasm', label: 'Sarcasm', desc: 'Sincere vs Snarky' },
                                    { key: 'sharpness', label: 'Sharpness', desc: 'Soft vs Witty/Cutting' },
                                    { key: 'intellect', label: 'Intellect', desc: 'Simple vs Genius' },
                                ].map(({ key, label, desc }) => {
                                    const val = waifuData.traits?.[key] ?? 0.5; // Default 0.5
                                    return (
                                        <div key={key} className="p-4 rounded-lg bg-zinc-50 border border-zinc-200 dark:bg-slate-800/50 dark:border-slate-700/50">
                                            <div className="flex justify-between items-center mb-2">
                                                <span className="font-medium text-zinc-700 dark:text-slate-200">{label}</span>
                                                <span className="font-mono text-sm text-purple-600 dark:text-purple-400">
                                                    {Math.round(val * 100)}%
                                                </span>
                                            </div>

                                            <input
                                                type="range" min="0" max="1" step="0.05"
                                                value={val}
                                                onChange={e => handleTraitChange(key, e.target.value)}
                                                className="w-full h-2 rounded-lg appearance-none cursor-pointer accent-purple-500 bg-zinc-200 dark:bg-slate-700"
                                            />

                                            <p className="text-xs mt-2 text-zinc-400 dark:text-slate-500">{desc}</p>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    )}
                </div>

                {/* Footer */}
                <div className="p-6 border-t flex justify-end bg-white border-zinc-200 dark:bg-slate-900 dark:border-slate-800">
                    <button
                        onClick={handleSave}
                        disabled={loading}
                        className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 px-6 py-2.5 rounded-lg text-white font-medium transition-colors disabled:opacity-50"
                    >
                        <Save size={18} />
                        {loading ? 'Saving...' : 'Save Changes'}
                    </button>
                </div>
            </div>
        </div>
    );
}
