import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import DashboardLayout from './components/DashboardLayout';
import OverviewPage from './pages/OverviewPage';
import EDAPage from './pages/EDAPage';
import SegmentationPage from './pages/SegmentationPage';
import MLPerformancePage from './pages/MLPerformancePage';
import RiskExplorerPage from './pages/RiskExplorerPage';
import LiveScoringPage from './pages/LiveScoringPage';

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await axios.get(`${API_URL}/analytics/`);
        setAnalyticsData(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="app-container justify-center items-center">
        <div className="spinner"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-container justify-center items-center">
        <div className="card" style={{ maxWidth: '400px', textAlign: 'center' }}>
          <h2 className="text-gradient" style={{ marginBottom: '0.5rem' }}>Error Loading Analytics</h2>
          <p style={{ color: 'var(--text-muted)' }}>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardLayout />}>
          <Route index element={<OverviewPage data={analyticsData} />} />
          <Route path="eda" element={<EDAPage data={analyticsData} />} />
          <Route path="segmentation" element={<SegmentationPage data={analyticsData} />} />
          <Route path="ml-performance" element={<MLPerformancePage data={analyticsData} />} />
          <Route path="risk-explorer" element={<RiskExplorerPage data={analyticsData} />} />
          <Route path="live-scoring" element={<LiveScoringPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
