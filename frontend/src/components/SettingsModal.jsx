import React, { useState, useEffect } from 'react';
import { X, User, Sparkles, Save } from 'lucide-react';
import clsx from 'clsx';
import * as api from '../api/client';

export default function SettingsModal({ onClose }) {
    const [activeTab, setActiveTab] = useState('user'); // 'user' | 'waifu'
    const [userData, setUserData] = useState({ username: '', bio: '' });
    const [waifuData, setWaifuData] = useState({ name: '', system_instruction: '', traits: {} });
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

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
            <div className="bg-slate-900 border border-slate-700 w-full max-w-2xl rounded-2xl shadow-2xl flex flex-col overflow-hidden max-h-[85vh]">

                {/* Header */}
                <div className="flex items-center justify-between p-6 border-b border-slate-800 bg-slate-900">
                    <h2 className="text-xl font-bold text-white">Settings</h2>
                    <button onClick={onClose} className="text-slate-400 hover:text-white">
                        <X size={24} />
                    </button>
                </div>

                {/* Tabs */}
                <div className="flex border-b border-slate-800 bg-slate-900/50">
                    <button
                        onClick={() => setActiveTab('user')}
                        className={clsx(
                            "flex-1 py-4 flex items-center justify-center gap-2 text-sm font-medium transition-colors",
                            activeTab === 'user' ? "text-indigo-400 border-b-2 border-indigo-500 bg-slate-800/50" : "text-slate-400 hover:text-slate-200"
                        )}
                    >
                        <User size={18} /> User Profile
                    </button>
                    <button
                        onClick={() => setActiveTab('waifu')}
                        className={clsx(
                            "flex-1 py-4 flex items-center justify-center gap-2 text-sm font-medium transition-colors",
                            activeTab === 'waifu' ? "text-purple-400 border-b-2 border-purple-500 bg-slate-800/50" : "text-slate-400 hover:text-slate-200"
                        )}
                    >
                        <Sparkles size={18} /> Waifu Persona
                    </button>
                </div>

                {/* Content */}
                <div className="p-6 overflow-y-auto flex-1 bg-slate-900">
                    {msg && (
                        <div className={clsx("mb-4 p-3 rounded text-sm", msg.type === 'error' ? "bg-red-900/30 text-red-200" : "bg-green-900/30 text-green-200")}>
                            {msg.text}
                        </div>
                    )}

                    {activeTab === 'user' ? (
                        <div className="space-y-4">
                            <label className="block">
                                <span className="text-slate-400 text-sm">Username</span>
                                <input
                                    type="text"
                                    value={userData.username}
                                    onChange={e => setUserData({ ...userData, username: e.target.value })}
                                    className="mt-1 w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-white focus:outline-none focus:border-indigo-500"
                                />
                            </label>
                            <label className="block">
                                <span className="text-slate-400 text-sm">Bio</span>
                                <textarea
                                    rows={3}
                                    value={userData.bio}
                                    onChange={e => setUserData({ ...userData, bio: e.target.value })}
                                    className="mt-1 w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-white focus:outline-none focus:border-indigo-500"
                                />
                            </label>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            <label className="block">
                                <span className="text-slate-400 text-sm">Name</span>
                                <input
                                    type="text"
                                    value={waifuData.name}
                                    onChange={e => setWaifuData({ ...waifuData, name: e.target.value })}
                                    className="mt-1 w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-white focus:outline-none focus:border-purple-500"
                                />
                            </label>
                            <label className="block">
                                <span className="text-slate-400 text-sm">System Instruction</span>
                                <textarea
                                    rows={5}
                                    value={waifuData.system_instruction}
                                    onChange={e => setWaifuData({ ...waifuData, system_instruction: e.target.value })}
                                    className="mt-1 w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-white focus:outline-none focus:border-purple-500 font-mono text-sm"
                                />
                            </label>

                            {/* Traits Demo (Only Sharpness/Intellect for now based on backend default) */}
                            <div className="grid grid-cols-2 gap-4">
                                {Object.entries(waifuData.traits || {}).map(([trait, val]) => (
                                    <label key={trait} className="block">
                                        <span className="text-slate-400 text-sm capitalize">{trait} ({val})</span>
                                        <input
                                            type="range" min="0" max="1" step="0.1"
                                            value={val}
                                            onChange={e => handleTraitChange(trait, e.target.value)}
                                            className="w-full mt-2 accent-purple-500"
                                        />
                                    </label>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                {/* Footer */}
                <div className="p-6 border-t border-slate-800 bg-slate-900 flex justify-end">
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
