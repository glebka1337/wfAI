import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import * as api from '../api/client';

const ChatContext = createContext();

export const useChat = () => useContext(ChatContext);

export const ChatProvider = ({ children }) => {
    const [sessions, setSessions] = useState([]);
    const [currentSessionId, setCurrentSessionId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isStreaming, setIsStreaming] = useState(false);
    const [connectionError, setConnectionError] = useState(null);
    const [personaIconUrl, setPersonaIconUrl] = useState(null);

    // Initial Load
    useEffect(() => {
        loadSessions();
        loadPersonaIcon();
    }, []);

    // Load messages when session changes
    useEffect(() => {
        if (currentSessionId) {
            loadHistory(currentSessionId);
        } else {
            setMessages([]);
        }
    }, [currentSessionId]);

    const loadSessions = async () => {
        try {
            setConnectionError(null);
            const data = await api.fetchSessions();
            setSessions(data.items || []);
        } catch (e) {
            console.error(e);
            setConnectionError("Cannot connect to Backend. Is it running?");
        }
    };

    const loadHistory = async (id) => {
        setIsLoading(true);
        try {
            const history = await api.fetchChatHistory(id);
            // Normalize roles: backend 'assistant' -> frontend 'ai'
            const normalizedHistory = history.map(msg => ({
                ...msg,
                role: msg.role === 'assistant' ? 'ai' : msg.role
            }));
            setMessages(normalizedHistory);
        } catch (e) {
            console.error(e);
        } finally {
            setIsLoading(false);
        }
    };

    const createNewSession = async () => {
        try {
            const session = await api.createSession();
            setSessions([session, ...sessions]); // Prepend
            setCurrentSessionId(session.uid);
            return session.uid;
        } catch (e) {
            console.error(e);
        }
    };

    const deleteSession = async (id) => {
        if (!confirm('Are you sure you want to delete this chat?')) return;
        try {
            await api.deleteSession(id);
            setSessions(sessions.filter(s => s.uid !== id));
            if (currentSessionId === id) setCurrentSessionId(null);
        } catch (e) {
            console.error(e);
        }
    };

    const sendMessage = async (content) => {
        if (!content.trim()) return;

        let sessionId = currentSessionId;

        // Auto-create session if none selected
        if (!sessionId) {
            sessionId = await createNewSession();
            if (!sessionId) return;
        }

        // Optimistic User Message
        const userMsg = { role: 'user', content };
        setMessages(prev => [...prev, userMsg]);
        setIsStreaming(true);

        try {
            // Placeholder for AI Message
            setMessages(prev => [...prev, { role: 'ai', content: '' }]);

            // Stream response
            let fullResponse = "";
            for await (const chunk of api.streamChat(sessionId, content)) {
                fullResponse += chunk;

                // Update last message (AI) with accumulated text
                setMessages(prev => {
                    const newMsgs = [...prev];
                    const lastMsg = newMsgs[newMsgs.length - 1];
                    lastMsg.content = fullResponse;
                    return newMsgs;
                });
            }
        } catch (e) {
            console.error(e);
            setMessages(prev => [...prev, { role: 'system', content: 'Error: Failed to send message' }]);
        } finally {
            setIsStreaming(false);
        }
    };

    const loadPersonaIcon = async () => {
        try {
            const persona = await api.fetchWaifuPersona();
            setPersonaIconUrl(persona.icon_url);
        } catch (e) {
            console.error('Failed to load persona icon:', e);
        }
    };

    const handleSetPersonaIcon = async (iconFilename) => {
        try {
            const updatedPersona = await api.setPersonaIcon(iconFilename);
            setPersonaIconUrl(updatedPersona.icon_url);
        } catch (e) {
            console.error('Failed to set persona icon:', e);
            throw e;
        }
    };

    return (
        <ChatContext.Provider value={{
            sessions,
            currentSessionId,
            setCurrentSessionId,
            messages,
            isLoading,
            isStreaming,
            connectionError,
            createNewSession,
            deleteSession,
            sendMessage,
            personaIconUrl,
            setPersonaIcon: handleSetPersonaIcon
        }}>
            {children}
        </ChatContext.Provider>
    );
};
