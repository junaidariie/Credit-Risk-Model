import { create } from 'zustand';
import { v4 as uuidv4 } from 'uuid';

const useStore = create((set) => ({
  token: localStorage.getItem('token') || null,
  user:  JSON.parse(localStorage.getItem('user') || 'null'),

  setAuth: (token, user) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    set({ token, user });
  },
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    set({ token: null, user: null });
  },

  // ── Prediction session (persists across tab navigation) ──
  prediction:   null,
  advisorText:  '',
  predictResult: null,   // raw result object {probability, credit_score, rating}
  setPrediction:   (p) => set({ prediction: p }),
  setAdvisorText:  (t) => set({ advisorText: t }),
  setPredictResult:(r) => set({ predictResult: r }),

  // ── Chat session (persists across tab navigation) ──
  chatMessages: [],
  chatThreadId: uuidv4(),
  setChatMessages: (msgs) => set({ chatMessages: msgs }),
  addChatMessage:  (msg)  => set((s) => ({ chatMessages: [...s.chatMessages, msg] })),
  updateLastChatMessage: (text) => set((s) => {
    const msgs = [...s.chatMessages];
    msgs[msgs.length - 1] = { ...msgs[msgs.length - 1], text };
    return { chatMessages: msgs };
  }),

  // ── Reset everything (New Assessment) ──
  resetSession: () => set({
    prediction:    null,
    advisorText:   '',
    predictResult: null,
    chatMessages:  [],
    chatThreadId:  uuidv4(),
  }),

  // ── TTS settings ──
  ttsVoice:  'en-GB-SoniaNeural',
  ttsRate:   '+0%',
  ttsVolume: '+0%',
  setTtsVoice:  (v) => set({ ttsVoice: v }),
  setTtsRate:   (r) => set({ ttsRate: r }),
  setTtsVolume: (v) => set({ ttsVolume: v }),

  // ── STT settings ──
  sttTranslation: false,
  sttLangDetect:  false,
  setSttTranslation: (v) => set({ sttTranslation: v }),
  setSttLangDetect:  (v) => set({ sttLangDetect: v }),
}));

export default useStore;
