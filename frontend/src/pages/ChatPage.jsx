import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Mic, MicOff, Volume2, Square, Sparkles } from 'lucide-react';
import { v4 as uuidv4 } from 'uuid';
import ReactMarkdown from 'react-markdown';
import useStore from '../store';
import { BASE } from '../api';
import './ChatPage.css';

const SUGGESTIONS = [
  'How can I improve my credit score?',
  'What does my default probability mean?',
  'Tips to reduce my delinquency ratio?',
  'How does loan type affect my rating?',
];

export default function ChatPage() {
  const {
    token, prediction, advisorText,
    ttsVoice, ttsRate, ttsVolume,
    sttTranslation, sttLangDetect,
    chatMessages, chatThreadId,
    addChatMessage, updateLastChatMessage, setChatMessages,
  } = useStore();

  const [input, setInput]         = useState('');
  const [sending, setSending]     = useState(false);
  const [recording, setRecording] = useState(false);
  const [sttStatus, setSttStatus] = useState('');
  const [ttsState, setTtsState]   = useState('idle');
  const [ttsTarget, setTtsTarget] = useState(null);

  const bottomRef = useRef(null);
  const mediaRef  = useRef(null);
  const chunksRef = useRef([]);
  const audioRef  = useRef(null);
  const inputRef  = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  const sendMessage = async (text) => {
    const msg = (text || input).trim();
    if (!msg || sending) return;
    if (!prediction) {
      addChatMessage({ role: 'system', text: 'Run a prediction first to unlock the advisor chat.', id: uuidv4() });
      return;
    }
    addChatMessage({ role: 'user', text: msg, id: uuidv4() });
    setInput('');
    setSending(true);
    addChatMessage({ role: 'assistant', text: '', id: uuidv4() });

    try {
      const res = await fetch(`${BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({
          thread_id: chatThreadId, message: msg,
          probability: prediction.probability,
          credit_score: prediction.credit_score,
          rating: prediction.rating,
          advisor_reply: advisorText,
        }),
      });
      const reader  = res.body.getReader();
      const decoder = new TextDecoder();
      let full = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        full += decoder.decode(value);
        updateLastChatMessage(full);
      }
    } catch {
      updateLastChatMessage('⚠️ Error getting response.');
    } finally {
      setSending(false);
      inputRef.current?.focus();
    }
  };

  /* ── STT ── */
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mr = new MediaRecorder(stream);
      chunksRef.current = [];
      mr.ondataavailable = (e) => chunksRef.current.push(e.data);
      mr.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        setSttStatus('transcribing');
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        const fd = new FormData();
        fd.append('file_path', blob, 'audio.webm');
        try {
          const res  = await fetch(
            `${BASE}/stt?translation=${sttTranslation}&language_detection=${sttLangDetect}`,
            { method: 'POST', headers: { Authorization: `Bearer ${token}` }, body: fd }
          );
          const data = await res.json();
          const transcribed = data.segments?.join(' ') || '';
          setInput(transcribed);

          // Build STT metadata to attach to the next user message
          // We store it temporarily so sendMessage can pick it up
          const meta = [];
          if (sttTranslation)                          meta.push({ type: 'translated', label: 'Translated to English' });
          if (sttLangDetect && data.detected_language) meta.push({ type: 'language',   label: `Language detected: ${data.detected_language}` });
          window.__sttMeta = meta.length ? meta : null;
        } catch {}
        setSttStatus('');
        inputRef.current?.focus();
      };
      mr.start();
      mediaRef.current = mr;
      setRecording(true);
      setSttStatus('recording');
    } catch {}
  };
  const stopRecording = () => { mediaRef.current?.stop(); setRecording(false); };

  /* Override sendMessage to attach STT meta when present */
  const sendWithMeta = async (text) => {
    const msg = (text || input).trim();
    if (!msg || sending) return;
    if (!prediction) {
      addChatMessage({ role: 'system', text: 'Run a prediction first to unlock the advisor chat.', id: uuidv4() });
      return;
    }
    const sttMeta = window.__sttMeta || null;
    window.__sttMeta = null;

    addChatMessage({ role: 'user', text: msg, sttMeta, id: uuidv4() });
    setInput('');
    setSending(true);
    addChatMessage({ role: 'assistant', text: '', id: uuidv4() });

    try {
      const res = await fetch(`${BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({
          thread_id: chatThreadId, message: msg,
          probability: prediction.probability,
          credit_score: prediction.credit_score,
          rating: prediction.rating,
          advisor_reply: advisorText,
        }),
      });
      const reader  = res.body.getReader();
      const decoder = new TextDecoder();
      let full = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        full += decoder.decode(value);
        updateLastChatMessage(full);
      }
    } catch {
      updateLastChatMessage('⚠️ Error getting response.');
    } finally {
      setSending(false);
      inputRef.current?.focus();
    }
  };

  /* ── TTS ── */
  const playTTS = async (text, idx) => {
    if (ttsState === 'playing' && ttsTarget === idx) {
      audioRef.current?.pause(); setTtsState('idle'); setTtsTarget(null); return;
    }
    setTtsState('loading'); setTtsTarget(idx);
    try {
      const res  = await fetch(`${BASE}/tts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ text, voice: ttsVoice, rate: ttsRate, volume: ttsVolume }),
      });
      const blob = await res.blob();
      audioRef.current.src = URL.createObjectURL(blob);
      audioRef.current.play();
      setTtsState('playing');
      audioRef.current.onended = () => { setTtsState('idle'); setTtsTarget(null); };
    } catch { setTtsState('idle'); setTtsTarget(null); }
  };

  const isEmpty = chatMessages.length === 0;

  return (
    <div className="chat-root">
      <audio ref={audioRef} style={{ display: 'none' }} />

      <div className="chat-messages">
        {/* Welcome state */}
        {isEmpty && (
          <div className="chat-welcome">
            <motion.div className="chat-welcome-icon"
              initial={{ scale: 0.7, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
              transition={{ type: 'spring', stiffness: 300, damping: 22 }}>
              <Sparkles size={28} />
            </motion.div>
            <motion.h3 className="chat-welcome-title"
              initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
              Conversational Advisor
            </motion.h3>
            <motion.p className="chat-welcome-sub"
              initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.18 }}>
              {prediction ? 'Ask me anything about your credit profile' : 'Run a prediction first to unlock the advisor'}
            </motion.p>
            {prediction && (
              <motion.div className="chat-chips"
                initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.28 }}>
                {SUGGESTIONS.map((s, i) => (
                  <motion.button key={i} className="chat-chip"
                    onClick={() => sendWithMeta(s)} whileTap={{ scale: 0.95 }}
                    initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 + i * 0.06 }}>
                    {s}
                  </motion.button>
                ))}
              </motion.div>
            )}
          </div>
        )}

        <AnimatePresence initial={false}>
          {chatMessages.map((msg, i) => (
            <motion.div key={msg.id}
              className={`chat-row chat-row--${msg.role}`}
              initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.24, ease: [0.22, 1, 0.36, 1] }}>

              {msg.role === 'system' && (
                <div className="chat-system-msg">{msg.text}</div>
              )}

              {msg.role === 'user' && (
                <div className="chat-user-group">
                  <div className="chat-bubble chat-bubble--user">{msg.text}</div>
                  {/* STT metadata tags */}
                  {msg.sttMeta && msg.sttMeta.length > 0 && (
                    <div className="chat-stt-meta">
                      {msg.sttMeta.map((m, mi) => (
                        <span key={mi} className={`chat-stt-tag chat-stt-tag--${m.type}`}>
                          {m.type === 'translated' ? '🌐' : '🔍'} {m.label}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {msg.role === 'assistant' && (
                <div className="chat-assistant-row">
                  <div className="chat-bot-avatar"><Sparkles size={13} /></div>
                  <div className="chat-bubble chat-bubble--assistant">
                    {msg.text
                      ? <>
                          <div className="md-body"><ReactMarkdown>{msg.text}</ReactMarkdown></div>
                          <button
                            className={`chat-tts-btn ${ttsState !== 'idle' && ttsTarget === i ? ttsState : ''}`}
                            onClick={() => playTTS(msg.text, i)}>
                            {ttsState === 'loading' && ttsTarget === i ? <span className="chat-spinner" />
                              : ttsState === 'playing' && ttsTarget === i ? <Square size={11} fill="currentColor" />
                              : <Volume2 size={12} />}
                          </button>
                        </>
                      : <span className="chat-typing"><span /><span /><span /></span>
                    }
                  </div>
                </div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>
        <div ref={bottomRef} />
      </div>

      {/* Input area */}
      <div className="chat-input-area">
        <AnimatePresence>
          {sttStatus && (
            <motion.div className={`chat-stt-bar ${sttStatus}`}
              initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}>
              {sttStatus === 'recording'    && <><span className="chat-stt-dot" /> Listening…</>}
              {sttStatus === 'transcribing' && <><span className="chat-spinner chat-spinner--blue" /> Transcribing your audio…</>}
            </motion.div>
          )}
        </AnimatePresence>

        <div className="chat-input-row">
          <motion.button
            className={`chat-mic-btn ${recording ? 'active' : ''}`}
            onClick={recording ? stopRecording : startRecording}
            whileTap={{ scale: 0.88 }}
            animate={recording
              ? { boxShadow: ['0 0 0 0 rgba(255,59,48,0.5)', '0 0 0 14px rgba(255,59,48,0)'] }
              : { boxShadow: '0 0 0 0 rgba(255,59,48,0)' }}
            transition={recording ? { duration: 1.2, repeat: Infinity } : {}}>
            {recording ? <MicOff size={18} /> : <Mic size={18} />}
          </motion.button>

          <div className="chat-input-box">
            <input
              ref={inputRef}
              className="chat-input"
              placeholder="Ask about your credit profile…"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && sendWithMeta()}
              disabled={sttStatus !== ''}
            />
          </div>

          <motion.button
            className={`chat-send-btn ${input.trim() && !sending ? 'active' : ''}`}
            onClick={() => sendWithMeta()}
            disabled={!input.trim() || sending}
            whileTap={{ scale: 0.88 }}>
            {sending ? <span className="chat-spinner" /> : <Send size={17} />}
          </motion.button>
        </div>
      </div>
    </div>
  );
}
