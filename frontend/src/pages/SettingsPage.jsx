import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Volume2, Mic, ChevronRight, X, Check, LogOut } from 'lucide-react';
import useStore from '../store';
import api from '../api';
import { useNavigate } from 'react-router-dom';
import './SettingsPage.css';

function groupVoices(voices) {
  const labels = {
    'en-GB':'English (British)','en-US':'English (US)','en-AU':'English (Australian)',
    'en-IN':'English (Indian)','hi-IN':'Hindi','ar-SA':'Arabic','ar-EG':'Arabic (Egypt)',
    'ru-RU':'Russian','de-DE':'German','fr-FR':'French','es-ES':'Spanish',
    'zh-CN':'Chinese','ja-JP':'Japanese','ko-KR':'Korean','pt-BR':'Portuguese',
    'it-IT':'Italian','tr-TR':'Turkish','pl-PL':'Polish','nl-NL':'Dutch',
    'sv-SE':'Swedish','nb-NO':'Norwegian','da-DK':'Danish','fi-FI':'Finnish',
  };
  const groups = {};
  for (const v of voices) {
    const key   = v.Voice.split('-').slice(0,2).join('-');
    const label = labels[key] || key;
    if (!groups[label]) groups[label] = [];
    groups[label].push(v);
  }
  return Object.entries(groups).sort((a,b) => a[0].localeCompare(b[0]));
}

function Toggle({ value, onChange, label, sub }) {
  return (
    <div className="s-row">
      <div className="s-row-text">
        <p className="s-row-label">{label}</p>
        {sub && <p className="s-row-sub">{sub}</p>}
      </div>
      <button className={`s-toggle ${value ? 'on' : ''}`} onClick={() => onChange(!value)}>
        <motion.div
          className="s-toggle-thumb"
          animate={{ x: value ? 20 : 2 }}
          transition={{ type: 'spring', stiffness: 500, damping: 35 }}
        />
      </button>
    </div>
  );
}

function SliderRow({ label, value, onChange, min, max, step, format }) {
  return (
    <div className="s-slider-row">
      <div className="s-slider-header">
        <span className="s-row-label">{label}</span>
        <span className="s-slider-val">{format ? format(value) : value}</span>
      </div>
      <input type="range" min={min} max={max} step={step} value={value}
        onChange={(e) => onChange(e.target.value)} className="s-slider" />
    </div>
  );
}

/* ── Voice picker modal ── */
function VoiceModal({ groups, current, onSelect, onClose }) {
  const [search, setSearch] = useState('');
  const [openGroup, setOpenGroup] = useState(null);

  const filtered = groups.map(([g, list]) => [
    g, list.filter((v) => v.Voice.toLowerCase().includes(search.toLowerCase()))
  ]).filter(([, list]) => list.length > 0);

  return (
    <AnimatePresence>
      <motion.div
        className="modal-overlay"
        initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
        onClick={onClose}
      >
        <motion.div
          className="modal-sheet"
          initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
          transition={{ type: 'spring', stiffness: 380, damping: 38 }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="modal-handle" />
          <div className="modal-header">
            <h3 className="modal-title">Select Voice</h3>
            <button className="modal-close" onClick={onClose}><X size={18} /></button>
          </div>
          <div className="modal-search-wrap">
            <input
              className="modal-search"
              placeholder="Search voices…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              autoFocus
            />
          </div>
          <div className="modal-body">
            {filtered.map(([group, list]) => (
              <div key={group} className="modal-group">
                <button
                  className="modal-group-header"
                  onClick={() => setOpenGroup(openGroup === group ? null : group)}
                >
                  <span>{group}</span>
                  <motion.div animate={{ rotate: openGroup === group ? 90 : 0 }}>
                    <ChevronRight size={14} />
                  </motion.div>
                </button>
                <AnimatePresence>
                  {openGroup === group && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                      style={{ overflow: 'hidden' }}
                    >
                      {list.map((v) => (
                        <button
                          key={v.Voice}
                          className={`modal-voice-item ${current === v.Voice ? 'active' : ''}`}
                          onClick={() => { onSelect(v.Voice); onClose(); }}
                        >
                          <div>
                            <span className="modal-voice-name">{v.Voice.split('-').slice(2).join('-')}</span>
                            <span className="modal-voice-gender">{v.Gender}</span>
                          </div>
                          {current === v.Voice && <Check size={15} className="modal-check" />}
                        </button>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ))}
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

/* ── Logout confirm modal ── */
function LogoutModal({ onConfirm, onCancel }) {
  return (
    <AnimatePresence>
      <motion.div
        className="modal-overlay modal-overlay--center"
        initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
        onClick={onCancel}
      >
        <motion.div
          className="logout-modal"
          initial={{ scale: 0.88, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.88, opacity: 0 }}
          transition={{ type: 'spring', stiffness: 420, damping: 30 }}
          onClick={(e) => e.stopPropagation()}
        >
          <h3 className="logout-modal-title">Sign Out</h3>
          <p className="logout-modal-sub">Are you sure you want to sign out?</p>
          <div className="logout-modal-actions">
            <button className="ios-btn ios-btn--ghost logout-modal-btn" onClick={onCancel}>Cancel</button>
            <button className="ios-btn ios-btn--primary logout-modal-btn" onClick={onConfirm}>
              <LogOut size={15} /> Sign Out
            </button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

export default function SettingsPage() {
  const { ttsVoice, ttsRate, ttsVolume, setTtsVoice, setTtsRate, setTtsVolume,
          sttTranslation, sttLangDetect, setSttTranslation, setSttLangDetect, logout } = useStore();
  const navigate = useNavigate();
  const [voiceGroups, setVoiceGroups]     = useState([]);
  const [showVoiceModal, setShowVoiceModal] = useState(false);
  const [showLogoutModal, setShowLogoutModal] = useState(false);

  const rateNum = parseInt(ttsRate) || 0;
  const volNum  = parseInt(ttsVolume) || 0;
  const fmtPct  = (v) => `${Number(v) >= 0 ? '+' : ''}${Number(v)}%`;

  useEffect(() => {
    api.get('/tts_available_voices')
      .then((r) => setVoiceGroups(groupVoices(r.data.Voices || [])))
      .catch(() => {});
  }, []);

  const handleLogout = async () => {
    try { await api.post('/auth/logout'); } catch (_) {}
    logout(); navigate('/auth');
  };

  // Short display name for current voice
  const voiceShort = ttsVoice.split('-').slice(2).join('-');

  return (
    <div className="s-root">
      <h2 className="s-heading">Settings</h2>

      {/* TTS */}
      <div className="s-section">
        <div className="s-section-header"><Volume2 size={15} /><span>Text-to-Speech</span></div>

        <SliderRow label="Speed"  value={rateNum} onChange={(v) => setTtsRate(fmtPct(v))}  min={-50} max={100} step={5} format={fmtPct} />
        <SliderRow label="Volume" value={volNum}  onChange={(v) => setTtsVolume(fmtPct(v))} min={-50} max={50}  step={5} format={fmtPct} />

        <button className="s-row s-row--btn" onClick={() => setShowVoiceModal(true)}>
          <div className="s-row-text">
            <p className="s-row-label">Voice</p>
            <p className="s-row-sub">{voiceShort}</p>
          </div>
          <ChevronRight size={16} className="s-chevron" />
        </button>
      </div>

      {/* STT */}
      <div className="s-section">
        <div className="s-section-header"><Mic size={15} /><span>Speech-to-Text</span></div>
        <Toggle value={sttTranslation} onChange={setSttTranslation}
          label="Translation Mode" sub="Translate audio to English" />
        <Toggle value={sttLangDetect} onChange={setSttLangDetect}
          label="Language Detection" sub="Detect the spoken language" />
      </div>

      {/* Account */}
      <div className="s-section">
        <div className="s-section-header"><LogOut size={15} /><span>Account</span></div>
        <motion.button
          className="s-logout-btn ios-btn ios-btn--primary"
          onClick={() => setShowLogoutModal(true)}
          whileTap={{ scale: 0.97 }}
        >
          <LogOut size={16} /> Sign Out
        </motion.button>
      </div>

      {/* Modals */}
      {showVoiceModal && (
        <VoiceModal
          groups={voiceGroups}
          current={ttsVoice}
          onSelect={setTtsVoice}
          onClose={() => setShowVoiceModal(false)}
        />
      )}
      {showLogoutModal && (
        <LogoutModal
          onConfirm={handleLogout}
          onCancel={() => setShowLogoutModal(false)}
        />
      )}
    </div>
  );
}
