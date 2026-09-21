import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { User, Shield, Activity, Users, TrendingUp, ChevronLeft, ChevronRight, Calendar, DollarSign, Percent } from 'lucide-react';
import useStore from '../store';
import api from '../api';
import './ProfilePage.css';

const RATING_COLOR = { Excellent: '#30d158', Good: '#0a84ff', Average: '#ff9f0a', Poor: '#ff453a' };

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

function PredictionCard({ h }) {
  const [open, setOpen] = useState(false);
  return (
    <motion.div className="pred-card" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
      <div className="pred-card-header" onClick={() => setOpen(!open)}>
        <div className="pred-card-left">
          <span className="pred-score">{h.credit_score}</span>
          <div>
            <span className="pred-rating" style={{ color: RATING_COLOR[h.rating] || '#fff' }}>{h.rating}</span>
            <p className="pred-date"><Calendar size={11} /> {new Date(h.created_at).toLocaleString()}</p>
          </div>
        </div>
        <div className="pred-card-right">
          <span className="pred-prob" style={{ color: h.probability > 0.5 ? 'var(--accent-red)' : 'var(--accent-green)' }}>
            {(h.probability * 100).toFixed(1)}%
          </span>
          <p className="pred-prob-label">Default Prob.</p>
        </div>
        <motion.div animate={{ rotate: open ? 90 : 0 }} className="pred-chevron">
          <ChevronRight size={16} />
        </motion.div>
      </div>
      <AnimatePresence>
        {open && (
          <motion.div
            className="pred-details"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <div className="pred-details-grid">
              {[
                ['Age', h.age],
                ['Income', `₹${h.income?.toLocaleString()}`],
                ['Loan Amount', `₹${h.loan_amount?.toLocaleString()}`],
                ['Tenure', `${h.loan_tenure_months} mo`],
                ['Purpose', h.loan_purpose],
                ['Type', h.loan_type],
                ['Residence', h.residence_type],
                ['Utilization', `${(h.credit_utilization_ratio * 100).toFixed(0)}%`],
                ['Delinquency Ratio', h.delinquency_ratio],
                ['Avg DPD', h.avg_dpd_per_delinquency],
                ['Open Accounts', h.num_open_accounts],
              ].map(([k, v]) => (
                <div key={k} className="pred-detail-item">
                  <span className="pred-detail-key">{k}</span>
                  <span className="pred-detail-val">{v}</span>
                </div>
              ))}
            </div>
            {h.advisor_response && (
              <div className="pred-advisor">
                <p className="pred-advisor-label">AI Advisor Summary</p>
                <p className="pred-advisor-text">{h.advisor_response}</p>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

export default function ProfilePage() {
  const { user } = useStore();
  const isAdmin = user?.role === 'admin';

  const [history, setHistory]         = useState([]);
  const [adminStats, setAdminStats]   = useState(null);
  const [allUsers, setAllUsers]       = useState([]);
  const [allPreds, setAllPreds]       = useState([]);
  const [userPreds, setUserPreds]     = useState(null);   // { user, preds }
  const [promoting, setPromoting]     = useState(null);
  const [tab, setTab]                 = useState('history');

  useEffect(() => {
    api.get('/user/my-history').then((r) => setHistory(r.data)).catch(() => {});
    if (isAdmin) {
      api.get('/admin/stats').then((r) => setAdminStats(r.data)).catch(() => {});
      api.get('/admin/users').then((r) => setAllUsers(r.data)).catch(() => {});
    }
  }, [isAdmin]);

  useEffect(() => {
    if (isAdmin && tab === 'predictions' && allPreds.length === 0) {
      api.get('/admin/predictions').then((r) => setAllPreds(r.data)).catch(() => {});
    }
  }, [tab, isAdmin]);

  const openUserPreds = async (u) => {
    const r = await api.get(`/admin/user/${u.user_id}/predictions`).catch(() => ({ data: [] }));
    setUserPreds({ user: u, preds: r.data });
  };

  const promote = async (userId) => {
    setPromoting(userId);
    try {
      await api.put(`/admin/promote/${userId}`);
      setAllUsers((u) => u.map((x) => x.user_id === userId ? { ...x, role: 'admin' } : x));
    } catch {}
    setPromoting(null);
  };

  const TABS = isAdmin
    ? [['history', 'My History'], ['users', 'All Users'], ['predictions', 'All Predictions']]
    : [];

  return (
    <div className="profile-root">
      {/* Header */}
      <div className="profile-hero">
        <div className="profile-avatar">{user?.username?.[0]?.toUpperCase() || 'U'}</div>
        <div>
          <h2 className="profile-name">{user?.username}</h2>
          <div className={`profile-role-badge ${isAdmin ? 'admin' : 'user'}`}>
            {isAdmin ? <Shield size={12} /> : <User size={12} />}
            {user?.role}
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="profile-stats">
        <StatCard icon={Activity}   label="My Predictions"  value={history.length}               color="var(--accent-blue)" />
        {isAdmin && <StatCard icon={Users}     label="Total Users"     value={adminStats?.total_users}      color="var(--accent-purple)" />}
        {isAdmin && <StatCard icon={TrendingUp} label="All Predictions" value={adminStats?.total_predictions} color="var(--accent-green)" />}
      </div>

      {/* Tabs */}
      {isAdmin && (
        <div className="profile-tabs">
          {TABS.map(([t, label]) => (
            <button key={t} className={`profile-tab ${tab === t ? 'active' : ''}`} onClick={() => setTab(t)}>
              {label}
            </button>
          ))}
        </div>
      )}

      {/* ── My History ── */}
      {tab === 'history' && (
        <div className="profile-list">
          {history.length === 0
            ? <p className="profile-empty">No predictions yet. Run your first assessment!</p>
            : history.map((h) => <PredictionCard key={h.id} h={h} />)
          }
        </div>
      )}

      {/* ── All Users ── */}
      {tab === 'users' && isAdmin && (
        <div className="profile-list">
          {allUsers.map((u) => (
            <div key={u.user_id} className="profile-user-item">
              <div className="pui-avatar">{u.username[0].toUpperCase()}</div>
              <div className="pui-info">
                <p className="pui-name">{u.username}</p>
                <div className="pui-meta">
                  <span className={`pui-role ${u.role}`}>{u.role}</span>
                  <span className={`pui-active ${u.is_active ? 'yes' : 'no'}`}>
                    {u.is_active ? 'Active' : 'Inactive'}
                  </span>
                  <span className="pui-id">ID #{u.user_id}</span>
                </div>
              </div>
              <div className="pui-actions">
                <button className="pui-view-btn" onClick={() => openUserPreds(u)}>
                  View <ChevronRight size={13} />
                </button>
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
            </div>
          ))}
        </div>
      )}

      {/* ── All Predictions ── */}
      {tab === 'predictions' && isAdmin && (
        <div className="profile-list">
          {allPreds.length === 0
            ? <p className="profile-empty">No predictions found.</p>
            : allPreds.map((h) => (
                <div key={h.id} className="pred-wrapper">
                  <span className="pred-user-tag">User #{h.user_id}</span>
                  <PredictionCard h={h} />
                </div>
              ))
          }
        </div>
      )}

      {/* ── User predictions drill-down modal ── */}
      <AnimatePresence>
        {userPreds && (
          <motion.div className="modal-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            onClick={() => setUserPreds(null)}>
            <motion.div className="user-preds-sheet"
              initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
              transition={{ type: 'spring', stiffness: 380, damping: 38 }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="modal-handle" />
              <div className="up-header">
                <button className="up-back" onClick={() => setUserPreds(null)}>
                  <ChevronLeft size={18} /> Back
                </button>
                <div>
                  <h3 className="up-title">{userPreds.user.username}</h3>
                  <p className="up-sub">{userPreds.preds.length} prediction{userPreds.preds.length !== 1 ? 's' : ''}</p>
                </div>
              </div>
              <div className="up-body">
                {userPreds.preds.length === 0
                  ? <p className="profile-empty">No predictions for this user.</p>
                  : userPreds.preds.map((h) => <PredictionCard key={h.id} h={h} />)
                }
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
