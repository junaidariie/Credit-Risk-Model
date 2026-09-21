import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Volume2, Square, ChevronDown, RotateCcw } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import useStore from '../store';
import { BASE } from '../api';
import './PredictPage.css';

const DEFAULTS = {
  age: 30, income: 75000, loan_amount: 250000, loan_tenure_months: 36,
  avg_dpd_per_delinquency: 5, delinquency_ratio: 0.1,
  credit_utilization_ratio: 0.3, num_open_accounts: 3,
  residence_type: 'Owned', loan_purpose: 'Home', loan_type: 'Secured',
};
const RESIDENCE_TYPES = ['Owned', 'Rented', 'Mortgage'];
const LOAN_PURPOSES   = ['Home', 'Education', 'Auto', 'Personal', 'Business'];
const LOAN_TYPES      = ['Secured', 'Unsecured'];

const RATING_META = {
  Excellent: { color: '#30d158', glow: 'rgba(48,209,88,0.22)',  bg: 'rgba(48,209,88,0.12)',  bar: '#30d158' },
  Good:      { color: '#0a84ff', glow: 'rgba(10,132,255,0.22)', bg: 'rgba(10,132,255,0.12)', bar: '#0a84ff' },
  Average:   { color: '#ff9f0a', glow: 'rgba(255,159,10,0.22)', bg: 'rgba(255,159,10,0.12)', bar: '#ff9f0a' },
  Poor:      { color: '#ff3b30', glow: 'rgba(255,59,48,0.22)',  bg: 'rgba(255,59,48,0.12)',  bar: '#ff3b30' },
};

/* ── Score progress bar ── */
function ScoreBar({ score, color }) {
  const pct = Math.min(Math.max((score - 300) / 600, 0), 1);
  return (
    <div className="pp-score-bar-wrap">
      <div className="pp-score-bar-track">
        <motion.div
          className="pp-score-bar-fill"
          style={{ background: color }}
          initial={{ width: 0 }}
          animate={{ width: `${pct * 100}%` }}
          transition={{ duration: 1.2, ease: [0.4, 0, 0.2, 1] }}
        />
      </div>
      <div className="pp-score-bar-labels">
        <span>300</span><span>900</span>
      </div>
    </div>
  );
}

function SelectField({ label, value, onChange, options }) {
  return (
    <div className="pp-field">
      <label className="pp-label">{label}</label>
      <div className="pp-select-wrap">
        <select value={value} onChange={(e) => onChange(e.target.value)} className="pp-select">
          {options.map((o) => <option key={o} value={o}>{o}</option>)}
        </select>
        <ChevronDown size={13} className="pp-select-arrow" />
      </div>
    </div>
  );
}

function NumField({ label, value, onChange, step = 1, min = 0 }) {
  return (
    <div className="pp-field">
      <label className="pp-label">{label}</label>
      <input type="number" className="pp-input" value={value} min={min} step={step}
        onChange={(e) => onChange(e.target.value)} />
    </div>
  );
}

/* ── Stat box ── */
function StatBox({ label, value, tag, color, glow, delay = 0, extra }) {
  return (
    <motion.div
      className="pp-stat-box"
      style={{ '--sb-glow': glow }}
      initial={{ opacity: 0, y: 18, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ delay, duration: 0.38, ease: [0.22, 1, 0.36, 1] }}
    >
      <span className="pp-sb-label">{label}</span>
      <span className="pp-sb-value" style={{ color }}>{value}</span>
      {extra}
      <span className="pp-sb-tag" style={{ color, background: `${color}18` }}>{tag}</span>
    </motion.div>
  );
}

export default function PredictPage() {
  const {
    token, ttsVoice, ttsRate, ttsVolume,
    setPrediction, setAdvisorText, setPredictResult,
    predictResult, advisorText,
    resetSession,
  } = useStore();
  const [form, setForm]         = useState(DEFAULTS);
  const [loading, setLoading]   = useState(false);
  const [result, setResult]     = useState(predictResult);   // init from store
  const [advisor, setAdvisor]   = useState(advisorText);     // init from store
  const [ttsState, setTtsState] = useState('idle');
  const audioRef = useRef(null);
  const set = (k) => (v) => setForm((f) => ({ ...f, [k]: v }));

  const handleNewAssessment = () => {
    resetSession();
    setResult(null);
    setAdvisor('');
    setTtsState('idle');
    setForm(DEFAULTS);
  };

  const handlePredict = async () => {
    setLoading(true); setResult(null); setAdvisor(''); setTtsState('idle');
    const payload = {
      ...form,
      age: Number(form.age), income: Number(form.income),
      loan_amount: Number(form.loan_amount), loan_tenure_months: Number(form.loan_tenure_months),
      avg_dpd_per_delinquency: Number(form.avg_dpd_per_delinquency),
      delinquency_ratio: Number(form.delinquency_ratio),
      credit_utilization_ratio: Number(form.credit_utilization_ratio),
      num_open_accounts: Number(form.num_open_accounts),
    };
    try {
      const res = await fetch(`${BASE}/predict_credit_risk_stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(payload),
      });
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let partial = { probability: null, credit_score: null, rating: null };
      let advText = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const lines = decoder.decode(value).split('\n').filter(Boolean);
        for (const line of lines) {
          if (line.startsWith('probability:'))      partial.probability  = parseFloat(line.slice(12));
          else if (line.startsWith('credit_score:')) partial.credit_score = parseInt(line.slice(13));
          else if (line.startsWith('rating:'))      { partial.rating = line.slice(7).trim(); setResult({ ...partial }); }
          else if (line.startsWith('advisor:'))     { advText += line.slice(8); setAdvisor(advText); }
        }
      }
      setPrediction(partial); setAdvisorText(advText); setPredictResult(partial);
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  const handleTTS = async () => {
    if (ttsState === 'playing') { audioRef.current?.pause(); setTtsState('idle'); return; }
    if (!advisor) return;
    setTtsState('loading');
    try {
      const res  = await fetch(`${BASE}/tts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ text: advisor, voice: ttsVoice, rate: ttsRate, volume: ttsVolume }),
      });
      const blob = await res.blob();
      audioRef.current.src = URL.createObjectURL(blob);
      audioRef.current.play();
      setTtsState('playing');
      audioRef.current.onended = () => setTtsState('idle');
    } catch { setTtsState('idle'); }
  };

  const meta       = result ? (RATING_META[result.rating] || RATING_META.Average) : null;
  const isHighRisk  = result && result.probability > 0.5;

  return (
    <div className="pp-root">
      <audio ref={audioRef} style={{ display: 'none' }} />

      <div className="pp-page-header">
        <div className="pp-header-row">
          <div>
            <h2 className="pp-heading">Risk Assessment</h2>
            <p className="pp-sub">Enter applicant details and run the model</p>
          </div>
          {result && (
            <motion.button
              className="pp-new-btn"
              onClick={handleNewAssessment}
              whileTap={{ scale: 0.95 }}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <RotateCcw size={14} />
              New Assessment
            </motion.button>
          )}
        </div>
      </div>

      {/* Form */}
      <div className="pp-card">
        <p className="pp-section-title">Applicant Profile</p>
        <div className="pp-grid">
          <NumField label="Age"                   value={form.age}                      onChange={set('age')}                      min={18} />
          <NumField label="Annual Income (₹)"     value={form.income}                   onChange={set('income')}                   step={1000} />
          <NumField label="Loan Amount (₹)"       value={form.loan_amount}              onChange={set('loan_amount')}              step={1000} />
          <NumField label="Tenure (months)"       value={form.loan_tenure_months}       onChange={set('loan_tenure_months')} />
          <NumField label="Avg DPD / Delinquency" value={form.avg_dpd_per_delinquency}  onChange={set('avg_dpd_per_delinquency')}  step={0.1} />
          <NumField label="Delinquency Ratio"     value={form.delinquency_ratio}        onChange={set('delinquency_ratio')}        step={0.01} />
          <NumField label="Credit Utilization"    value={form.credit_utilization_ratio} onChange={set('credit_utilization_ratio')} step={0.01} />
          <NumField label="Open Accounts"         value={form.num_open_accounts}        onChange={set('num_open_accounts')} />
          <SelectField label="Residence Type" value={form.residence_type} onChange={set('residence_type')} options={RESIDENCE_TYPES} />
          <SelectField label="Loan Purpose"   value={form.loan_purpose}   onChange={set('loan_purpose')}   options={LOAN_PURPOSES} />
          <SelectField label="Loan Type"      value={form.loan_type}      onChange={set('loan_type')}      options={LOAN_TYPES} />
        </div>
        <motion.button
          className="pp-run-btn"
          onClick={handlePredict}
          disabled={loading}
          whileTap={{ scale: 0.96 }}
        >
          {loading
            ? <><span className="pp-spinner" /> Analysing…</>
            : <><Zap size={18} /> Run Prediction</>
          }
        </motion.button>
      </div>

      {/* Results */}
      <AnimatePresence>
        {result && (
          <motion.div
            className="pp-results"
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
          >
            {/* ── 3 stat boxes ── */}
            <div className="pp-stat-boxes">
              <StatBox
                label="Default Probability"
                value={`${(result.probability * 100).toFixed(1)}%`}
                tag={isHighRisk ? '⚠ High Risk' : '✓ Low Risk'}
                color={isHighRisk ? '#ff3b30' : '#30d158'}
                glow={isHighRisk ? 'rgba(255,59,48,0.18)' : 'rgba(48,209,88,0.18)'}
                delay={0.05}
              />
              <StatBox
                label="Credit Score"
                value={result.credit_score}
                tag="out of 900"
                color={meta.color}
                glow={meta.glow}
                delay={0.12}
                extra={<ScoreBar score={result.credit_score} color={meta.color} />}
              />
              <StatBox
                label="Risk Rating"
                value={result.rating}
                tag={result.rating === 'Excellent' ? '🏆 Top tier' : result.rating === 'Good' ? '✓ Solid' : result.rating === 'Average' ? '~ Moderate' : '⚠ Needs work'}
                color={meta.color}
                glow={meta.glow}
                delay={0.19}
              />
            </div>

            {/* ── AI Advisor card ── */}
            <div className="pp-advisor-card">
              <div className="pp-advisor-header">
                <div className="pp-advisor-title-row">
                  <div className="pp-advisor-dot" />
                  <span className="pp-advisor-title">AI Advisor</span>
                </div>
                {advisor && (
                  <motion.button
                    className={`pp-tts-btn ${ttsState !== 'idle' ? ttsState : ''}`}
                    onClick={handleTTS}
                    whileTap={{ scale: 0.92 }}
                  >
                    {ttsState === 'loading' && <span className="pp-spinner pp-spinner--sm pp-spinner--dark" />}
                    {ttsState === 'playing' && <Square size={13} fill="currentColor" />}
                    {ttsState === 'idle'    && <Volume2 size={14} />}
                    <span>{ttsState === 'playing' ? 'Stop' : ttsState === 'loading' ? 'Loading…' : 'Listen'}</span>
                  </motion.button>
                )}
              </div>
              <div className="pp-advisor-body">
                {advisor
                  ? <div className="md-body"><ReactMarkdown>{advisor}</ReactMarkdown></div>
                  : <div className="pp-advisor-streaming">
                      <span className="pp-spinner pp-spinner--sm pp-spinner--dark" />
                      Generating advisory…
                    </div>
                }
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
