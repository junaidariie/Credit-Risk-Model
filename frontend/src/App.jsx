import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import useStore from './store';
import AuthPage from './pages/AuthPage';
import MainLayout from './pages/MainLayout';

export default function App() {
  const token = useStore((s) => s.token);
  return (
    <Routes>
      <Route path="/auth" element={!token ? <AuthPage /> : <Navigate to="/" replace />} />
      <Route path="/*" element={token ? <MainLayout /> : <Navigate to="/auth" replace />} />
    </Routes>
  );
}
