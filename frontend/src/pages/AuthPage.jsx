import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, Eye, EyeOff, User, Lock, ArrowRight } from 'lucide-react';
import api from '../api';
import useStore from '../store';
import './AuthPage.css';

export default function AuthPage() {
  const [mode, setMode]     = useState('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPw, setShowPw] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError]   = useState('');
  const [success, setSuccess] = useState('');
  const setAuth = useStore((s) => s.setAuth);

  const reset = () => { setError(''); setSuccess(''); };

  const switchMode = (m) => { setMode(m); reset(); setUsername(''); setPassword(''); };

  const handleSubmit = async (e) => {
    e.preventDefault();
    reset();
    setLoading(true);
    try {
      if (mode === 'register') {
        await api.post('/auth/register', { username, password });
        setSuccess('Account created! Signing you in…');
        setMode('login');
      } else {
        const form = new URLSearchParams();
        form.append('username', username);
        form.append('password', password);
        const { data } = await api.post('/auth/login', form, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });
        const me = await api.get('/user/me', {
          headers: { Authorization: `Bearer ${data.access_token}` },
        });
        setAuth(data.access_token, me.data);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-root">
      {/* Animated background orbs */}
      <div className="auth-orb auth-orb-1" />
      <div className="auth-orb auth-orb-2" />
      <div className="auth-orb auth-orb-3" />

      {/* Glassmorphism card */}
      <motion.div
        className="auth-card"
        initial={{ opacity: 0, y: 48, scale: 0.94 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1] }}
      >
        {/* App icon */}
        <motion.div
          className="auth-icon-wrap"
          initial={{ scale: 0.6, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.15, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        >
          <div className="auth-icon-ring" />
          <div className="auth-icon-inner">
            <Shield size={30} strokeWidth={1.6} />
          </div>
        </motion.div>

        <motion.div
          className="auth-brand"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25, duration: 0.4 }}
        >
          <h1 className="auth-title">RiskGuard AI</h1>
          <p className="auth-subtitle">Credit Risk Intelligence Platform</p>
        </motion.div>

        {/* Segmented control */}
        <motion.div
          className="auth-seg"
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.32, duration: 0.4 }}
        >
          {['login', 'register'].map((t) => (
            <button
              key={t}
              className={`auth-seg-btn ${mode === t ? 'active' : ''}`}
              onClick={() => switchMode(t)}
            >
              {t === 'login' ? 'Sign In' : 'Create Account'}
            </button>
          ))}
          <motion.div
            className="auth-seg-indicator"
            animate={{ x: mode === 'login' ? 0 : '100%' }}
            transition={{ type: 'spring', stiffness: 420, damping: 36 }}
          />
        </motion.div>

        {/* Form */}
        <AnimatePresence mode="wait">
          <motion.form
            key={mode}
            initial={{ opacity: 0, x: mode === 'login' ? -24 : 24 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: mode === 'login' ? 24 : -24 }}
            transition={{ duration: 0.26, ease: [0.4, 0, 0.2, 1] }}
            className="auth-form"
            onSubmit={handleSubmit}
          >
            {/* Username */}
            <div className="auth-field-wrap">
              <label className="auth-field-label">Username</label>
              <div className="auth-field">
                <User size={15} className="auth-field-icon" />
                <input
                  type="text"
                  placeholder="Enter your username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required minLength={3} maxLength={20}
                  autoComplete="username"
                  autoCapitalize="none"
                />
              </div>
            </div>

            {/* Password */}
            <div className="auth-field-wrap">
              <label className="auth-field-label">Password</label>
              <div className="auth-field">
                <Lock size={15} className="auth-field-icon" />
                <input
                  type={showPw ? 'text' : 'password'}
                  placeholder={mode === 'register' ? 'Min. 8 characters' : 'Enter your password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required minLength={8}
                  autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
                />
                <button type="button" className="auth-eye" onClick={() => setShowPw(!showPw)}>
                  {showPw ? <EyeOff size={15} /> : <Eye size={15} />}
                </button>
              </div>
            </div>

            {/* Messages */}
            <AnimatePresence>
              {error && (
                <motion.div
                  className="auth-alert auth-alert--error"
                  initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <span className="auth-alert-dot" />
                  {error}
                </motion.div>
              )}
              {success && (
                <motion.div
                  className="auth-alert auth-alert--success"
                  initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <span className="auth-alert-dot" />
                  {success}
                </motion.div>
              )}
            </AnimatePresence>

            {/* Submit */}
            <motion.button
              type="submit"
              className="auth-submit"
              disabled={loading}
              whileTap={{ scale: 0.96 }}
              whileHover={{ scale: 1.015 }}
            >
              {loading
                ? <span className="auth-spinner" />
                : <>
                    <span>{mode === 'login' ? 'Sign In' : 'Create Account'}</span>
                    <ArrowRight size={18} />
                  </>
              }
            </motion.button>
          </motion.form>
        </AnimatePresence>

        {/* Footer switch */}
        <motion.p
          className="auth-switch"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}
        >
          {mode === 'login' ? "Don't have an account? " : 'Already have an account? '}
          <button className="auth-switch-btn" onClick={() => switchMode(mode === 'login' ? 'register' : 'login')}>
            {mode === 'login' ? 'Create one' : 'Sign in'}
          </button>
        </motion.p>
      </motion.div>
    </div>
  );
}
