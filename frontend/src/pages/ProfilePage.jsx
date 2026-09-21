import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { User, Shield, Activity, Users, TrendingUp, ChevronRight } from 'lucide-react';
import useStore from '../store';
import api from '../api';
import './ProfilePage.css';

function StatCard({ icon: Icon, label, value, color }) {
  return (
    <div className="profile-stat-card">
      <div className="profile-stat-icon" style={{ background: `${color}20`, color }}>
        <Icon size={18} />
      </div>
      <div>
        <p className="profile-stat-value">{value ?? '—'}</p>
        <p className="profile-stat-label">{label}</p>
      </div>
    </div>
  );
}

export default function ProfilePage() {
  const { user } = useStore();
  const isAdmin = user?.role === 'admin';
  const [history, setHistory] = useState([]);
  const [adminStats, setAdminStats] = useState(null);
  const [allUsers, setAllUsers] = useState([]);
  const [promoting, setPromoting] = useState(null);
  const [tab, setTab] = useState('history'); // history | users | predictions

  useEffect(() => {
    api.get('/user/my-history').then((r) => setHistory(r.data)).catch(() => {});
    if (isAdmin) {
      api.get('/admin/stats').then((r) => setAdminStats(r.data)).catch(() => {});
      api.get('/admin/users').then((r) => setAllUsers(r.data)).catch(() => {});
    }
  }, [isAdmin]);

  const promote = async (userId) => {
    setPromoting(userId);
    try {
      await api.put(`/admin/promote/${userId}`);
      setAllUsers((u) => u.map((x) => x.user_id === userId ? { ...x, role: 'admin' } : x));
    } catch {}
    setPromoting(null);
  };

  const RATING_COLOR = { Excellent: '#30d158', Good: '#0a84ff', Average: '#ff9f0a', Poor: '#ff453a' };

  return (
    <div className="profile-root">
      {/* Profile header */}
      <div className="profile-hero">
        <div className="profile-avatar">
          {user?.username?.[0]?.toUpperCase() || 'U'}
        </div>
        <div>
          <h2 className="profile-name">{user?.username}</h2>
          <div className={`profile-role-badge ${isAdmin ? 'admin' : 'user'}`}>
            {isAdmin ? <Shield size={12} /> : <User size={12} />}
            {user?.role}
          </div>
        </div>
      </div>

      {/* Stats row */}
      <div className="profile-stats">
        <StatCard icon={Activity} label="Predictions" value={history.length} color="var(--accent-blue)" />
        {isAdmin && <StatCard icon={Users} label="Total Users" value={adminStats?.total_users} color="var(--accent-purple)" />}
        {isAdmin && <StatCard icon={TrendingUp} label="All Predictions" value={adminStats?.total_predictions} color="var(--accent-green)" />}
      </div>

      {/* Tabs */}
      {isAdmin && (
        <div className="profile-tabs">
          {['history', 'users'].map((t) => (
            <button
              key={t}
              className={`profile-tab ${tab === t ? 'active' : ''}`}
              onClick={() => setTab(t)}
            >
              {t === 'history' ? 'My History' : 'All Users'}
            </button>
          ))}
        </div>
      )}

      {/* My prediction history */}
      {tab === 'history' && (
        <div className="profile-list">
          {history.length === 0 && (
            <p className="profile-empty">No predictions yet. Run your first assessment!</p>
          )}
          {history.map((h) => (
            <motion.div
              key={h.id}
              className="profile-history-item"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="phi-left">
                <span className="phi-score">{h.credit_score}</span>
                <div>
                  <span className="phi-rating" style={{ color: RATING_COLOR[h.rating] || '#fff' }}>{h.rating}</span>
                  <p className="phi-date">{new Date(h.created_at).toLocaleDateString()}</p>
                </div>
              </div>
              <div className="phi-right">
                <span className="phi-prob" style={{ color: h.probability > 0.5 ? 'var(--accent-red)' : 'var(--accent-green)' }}>
                  {(h.probability * 100).toFixed(1)}%
                </span>
                <p className="phi-prob-label">Default Prob.</p>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Admin: all users */}
      {tab === 'users' && isAdmin && (
        <div className="profile-list">
          {allUsers.map((u) => (
            <div key={u.user_id} className="profile-user-item">
              <div className="pui-avatar">{u.username[0].toUpperCase()}</div>
              <div className="pui-info">
                <p className="pui-name">{u.username}</p>
                <p className={`pui-role ${u.role}`}>{u.role}</p>
              </div>
              {u.role !== 'admin' && (
                <motion.button
                  className="pui-promote-btn"
                  onClick={() => promote(u.user_id)}
                  disabled={promoting === u.user_id}
                  whileTap={{ scale: 0.95 }}
                >
                  {promoting === u.user_id ? '…' : 'Promote'}
                </motion.button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
