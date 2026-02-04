/**
 * API Wrapper for Waifu AI Backend
 * Note: '/api' prefix is handled by Vite Proxy
 */

// Helper for standard JSON headers
const getHeaders = () => ({
    'Content-Type': 'application/json',
});

// --- SESSIONS ---
export const fetchSessions = async () => {
    const res = await fetch('/api/sessions');
    if (!res.ok) throw new Error('Failed to fetch sessions');
    return res.json();
};

export const createSession = async (title = 'New Chat') => {
    const res = await fetch('/api/sessions', {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ title }),
    });
    if (!res.ok) throw new Error('Failed to create session');
    return res.json();
};

export const deleteSession = async (sessionId) => {
    const res = await fetch(`/api/sessions/${sessionId}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete session');
    return true;
};

export const updateSession = async (sessionId, title) => {
    const res = await fetch(`/api/sessions/${sessionId}`, {
        method: 'PATCH',
        headers: getHeaders(),
        body: JSON.stringify({ title }),
    });
    if (!res.ok) throw new Error('Failed to update session');
    return res.json();
};

// --- CHAT ---
export const fetchChatHistory = async (sessionId) => {
    const res = await fetch(`/api/chat/${sessionId}/history`);
    if (!res.ok) throw new Error('Failed to fetch history');
    return res.json();
};

export const fetchCommands = async () => {
    const res = await fetch('/api/commands');
    if (!res.ok) throw new Error('Failed to fetch commands');
    return res.json();
};

export const fetchIcons = async () => {
    const res = await fetch('/api/icons');
    if (!res.ok) throw new Error("Failed to fetch icons");
    return res.json();
};

export const uploadIcon = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch('/api/icons', {
        method: 'POST',
        body: formData
    });
    if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || "Failed to upload icon");
    }
    return res.json();
};

export const deleteIcon = async (filename) => {
    const res = await fetch(`/api/icons/${filename}`, {
        method: 'DELETE'
    });
    if (!res.ok) throw new Error("Failed to delete icon");
    return res.json();
};

export const setPersonaIcon = async (iconFilename) => {
    const res = await fetch(`/api/settings/waifu/icon?icon_filename=${encodeURIComponent(iconFilename)}`, {
        method: 'PATCH',
        headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to set persona icon');
    return res.json();
};

/**
 * Streams chat response from backend.
 * Yields text chunks as they arrive.
 */
export async function* streamChat(sessionId, message) {
    const res = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ session_id: sessionId, message }),
    });

    if (!res.ok) throw new Error('Chat stream failed');

    const reader = res.body.getReader();
    const decoder = new TextDecoder('utf-8');

    while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        yield decoder.decode(value, { stream: true });
    }
}

// --- SETTINGS ---
export const fetchUserProfile = async () => {
    const res = await fetch('/api/settings/user');
    if (!res.ok) throw new Error('Failed to fetch user profile');
    return res.json();
};

export const updateUserProfile = async (data) => {
    const res = await fetch('/api/settings/user', {
        method: 'PATCH',
        headers: getHeaders(),
        body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to update user profile');
    return res.json();
};

export const fetchWaifuPersona = async () => {
    const res = await fetch('/api/settings/waifu');
    if (!res.ok) throw new Error('Failed to fetch waifu persona');
    return res.json();
};

export const updateWaifuPersona = async (data) => {
    const res = await fetch('/api/settings/waifu', {
        method: 'PATCH',
        headers: getHeaders(),
        body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to update waifu persona');
    return res.json();
};
