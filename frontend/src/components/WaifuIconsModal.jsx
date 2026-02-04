import React, { useState, useEffect } from 'react';
import { X, Upload, Trash2, Image as ImageIcon, Check } from 'lucide-react';
import { fetchIcons, uploadIcon, deleteIcon } from '../api/client';
import { useChat } from '../context/ChatContext';

export default function WaifuIconsModal({ onClose }) {
    const { personaIconUrl, setPersonaIcon } = useChat();
    const [icons, setIcons] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadIcons();
    }, []);

    const loadIcons = async () => {
        try {
            const data = await fetchIcons();
            setIcons(data);
        } catch (e) {
            console.error(e);
            setError("Failed to load icons.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        if (file.size > 5 * 1024 * 1024) {
            setError("File size exceeds 5MB limit.");
            return;
        }

        setIsUploading(true);
        setError(null);
        try {
            await uploadIcon(file);
            await loadIcons();
        } catch (e) {
            console.error(e);
            setError(e.message);
        } finally {
            setIsUploading(false);
        }
    };

    const handleDelete = async (url) => {
        if (!confirm("Are you sure you want to delete this icon?")) return;

        // Extract filename from URL
        const filename = url.split('/').pop();
        try {
            await deleteIcon(filename);
            await loadIcons();
        } catch (e) {
            console.error(e);
            setError("Failed to delete icon.");
        }
    };

    const handleSetAsCurrent = async (url) => {
        const filename = url.split('/').pop();
        try {
            await setPersonaIcon(filename);
        } catch (e) {
            console.error(e);
            setError("Failed to set icon as current.");
        }
    };

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50 backdrop-blur-sm">
            <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-2xl max-h-[80vh] flex flex-col shadow-2xl">

                {/* Header */}
                <div className="flex items-center justify-between p-4 border-b border-slate-700">
                    <div className="flex items-center gap-2">
                        <ImageIcon className="text-pink-400" size={20} />
                        <h2 className="text-xl font-semibold text-slate-100">Waifu Icons</h2>
                    </div>
                    <button onClick={onClose} className="p-1 hover:bg-slate-800 rounded-full text-slate-400 transition-colors">
                        <X size={20} />
                    </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-4">
                    {error && (
                        <div className="mb-4 p-3 bg-red-900/20 border border-red-800 text-red-200 rounded-lg text-sm">
                            {error}
                        </div>
                    )}

                    {isLoading ? (
                        <div className="text-center text-slate-500 py-8">Loading icons...</div>
                    ) : (
                        <div className="grid grid-cols-3 sm:grid-cols-4 gap-4">
                            {icons.map((url, index) => {
                                const isSelected = personaIconUrl === url;
                                return (
                                    <div key={index} className={`group relative aspect-square bg-slate-800 rounded-lg overflow-hidden border-2 transition-all ${isSelected ? 'border-indigo-500 ring-2 ring-indigo-500/50' : 'border-slate-700 hover:border-pink-500'
                                        }`}>
                                        <img src={url} alt="Waifu Icon" className="w-full h-full object-cover" />

                                        {/* Selected indicator */}
                                        {isSelected && (
                                            <div className="absolute top-2 right-2 bg-indigo-600 rounded-full p-1">
                                                <Check size={14} className="text-white" />
                                            </div>
                                        )}

                                        {/* Hover actions */}
                                        <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                                            {!isSelected && (
                                                <button
                                                    onClick={() => handleSetAsCurrent(url)}
                                                    className="px-3 py-1 bg-indigo-600 hover:bg-indigo-500 rounded text-white text-xs transition-colors"
                                                    title="Set as current icon"
                                                >
                                                    Set
                                                </button>
                                            )}
                                            <button
                                                onClick={() => handleDelete(url)}
                                                className="p-2 bg-red-600 hover:bg-red-500 rounded-full text-white transition-colors"
                                                title="Delete icon"
                                            >
                                                <Trash2 size={16} />
                                            </button>
                                        </div>
                                    </div>
                                );
                            })}

                            {/* Upload Placeholders */}
                            {icons.length === 0 && (
                                <div className="col-span-full text-center text-slate-500 py-8">
                                    No icons yet. Upload one below!
                                </div>
                            )}
                        </div>
                    )}
                </div>

                {/* Footer / Upload */}
                <div className="p-4 border-t border-slate-700 bg-slate-800/50">
                    <label className={`w-full flex items-center justify-center gap-2 p-3 bg-indigo-600 hover:bg-indigo-500 rounded-lg cursor-pointer transition-colors text-white font-medium ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}`}>
                        <Upload size={18} />
                        {isUploading ? 'Uploading...' : 'Upload New Icon'}
                        <input
                            type="file"
                            accept="image/png, image/jpeg"
                            className="hidden"
                            onChange={handleUpload}
                            disabled={isUploading}
                        />
                    </label>
                    <p className="text-center text-xs text-slate-500 mt-2">
                        Supported formats: PNG, JPG, JPEG. Max size: 5MB.
                    </p>
                </div>
            </div>
        </div>
    );
}
