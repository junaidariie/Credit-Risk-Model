import React from 'react';
import { Routes, Route, NavLink, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { BarChart2, MessageSquare, Settings, User } from 'lucide-react';
import useStore from '../store';
import PredictPage from './PredictPage';
import ChatPage from './ChatPage';
import SettingsPage from './SettingsPage';
import ProfilePage from './ProfilePage';
import './MainLayout.css';

const NAV = [
  { to: '/',         icon: BarChart2,     label: 'Assess'   },
  { to: '/chat',     icon: MessageSquare, label: 'Chat'     },
  { to: '/settings', icon: Settings,      label: 'Settings' },
];

export default function MainLayout() {
  const { user } = useStore();
  const navigate = useNavigate();

  return (
    <div className="layout-root">
      {/* ── Top navigation bar ── */}
      <header className="topbar">
        {/* Brand */}
        <div className="topbar-brand" onClick={() => navigate('/')} role="button" tabIndex={0}>
          <div className="topbar-logo-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
          </div>
          <span className="topbar-wordmark">RiskGuard</span>
          <span className="topbar-wordmark-ai">AI</span>
          {user?.role === 'admin' && <span className="topbar-badge">Admin</span>}
        </div>

        {/* Centre nav tabs */}
        <nav className="topbar-nav">
          {NAV.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              end
              className={({ isActive }) => `tnav-item ${isActive ? 'active' : ''}`}
            >
              {({ isActive }) => (
                <>
                  <Icon size={15} strokeWidth={isActive ? 2.3 : 1.8} />
                  <span>{label}</span>
                  {isActive && (
                    <motion.div
                      className="tnav-indicator"
                      layoutId="tnav-indicator"
                      transition={{ type: 'spring', stiffness: 500, damping: 38 }}
                    />
                  )}
                </>
              )}
            </NavLink>
          ))}
        </nav>

        {/* Right: profile icon */}
        <div className="topbar-right">
          <motion.button
            className="topbar-avatar-btn"
            onClick={() => navigate('/profile')}
            whileTap={{ scale: 0.92 }}
            title="Profile"
          >
            <span className="topbar-avatar-letter">
              {user?.username?.[0]?.toUpperCase() || 'U'}
            </span>
          </motion.button>
        </div>
      </header>

      {/* ── Page content ── */}
      <main className="layout-main">
        <Routes>
          <Route path="/"         element={<PredictPage />} />
          <Route path="/chat"     element={<ChatPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="/profile"  element={<ProfilePage />} />
        </Routes>
      </main>
    </div>
  );
}
