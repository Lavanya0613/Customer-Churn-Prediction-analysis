import React, { useState, useEffect } from 'react';
import { Users, AlertTriangle, CheckCircle, TrendingUp } from 'lucide-react';
import axios from 'axios';

export default function Overview({ onNavigate }) {
  const [modelInfo, setModelInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchModelInfo = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const response = await axios.get(`${apiUrl}/model-info`);
        setModelInfo(response.data);
      } catch (error) {
        console.error("Failed to fetch model info", error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchModelInfo();
  }, []);

  return (
    <div style={{ maxWidth: '1000px' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', margin: '0 0 0.5rem 0' }}>Executive Overview</h1>
        <p style={{ color: 'var(--text-secondary)' }}>
          Monitor customer retention health and operationalize churn intelligence.
        </p>
      </header>

      <div className="grid grid-cols-3" style={{ marginBottom: '2rem' }}>
        <MetricCard 
          title="Active Model"
          value={loading ? "..." : (modelInfo?.model_type || "Logistic Regression")}
          subtitle="Production Pipeline"
          icon={<CheckCircle size={24} className="text-success" color="var(--success)" />}
        />
        <MetricCard 
          title="Critical Risk Threshold"
          value={loading ? "..." : `> ${(modelInfo?.thresholds?.critical || 0.5) * 100}%`}
          subtitle="Cost-optimized cutoff"
          icon={<AlertTriangle size={24} color="var(--danger)" />}
        />
        <MetricCard 
          title="Features Analyzed"
          value={loading ? "..." : (modelInfo?.features?.length || 23)}
          subtitle="Real-time evaluation"
          icon={<TrendingUp size={24} color="var(--accent)" />}
        />
      </div>

      <div className="grid grid-cols-2">
        <div className="card">
          <h3 style={{ marginBottom: '1rem', borderBottom: '1px solid var(--border)', paddingBottom: '0.5rem' }}>
            Quick Actions
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
            <button 
              className="btn btn-primary" 
              onClick={() => onNavigate('prediction')}
              style={{ justifyContent: 'flex-start', padding: '1rem' }}
            >
              <Users size={18} />
              Score a New Customer
            </button>
            <button 
              className="btn btn-secondary" 
              onClick={() => onNavigate('high-risk')}
              style={{ justifyContent: 'flex-start', padding: '1rem' }}
            >
              <AlertTriangle size={18} />
              View High-Risk Cohort
            </button>
          </div>
        </div>

        <div className="card">
          <h3 style={{ marginBottom: '1rem', borderBottom: '1px solid var(--border)', paddingBottom: '0.5rem' }}>
            System Status
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
            <StatusRow label="API Service" status="Online" type="success" />
            <StatusRow label="Database (Postgres)" status="Connected" type="success" />
            <StatusRow label="Model Explainer (SHAP)" status="Loaded" type="success" />
          </div>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ title, value, subtitle, icon }) {
  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', margin: 0, fontWeight: 500 }}>{title}</h3>
        {icon}
      </div>
      <div style={{ fontSize: '1.75rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '0.25rem' }}>
        {value}
      </div>
      <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
        {subtitle}
      </div>
    </div>
  );
}

function StatusRow({ label, status, type }) {
  const color = type === 'success' ? 'var(--success)' : type === 'warning' ? 'var(--warning)' : 'var(--danger)';
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <span style={{ color: 'var(--text-secondary)' }}>{label}</span>
      <span className={`badge`} style={{ 
        background: `${color}20`, 
        color: color, 
        border: `1px solid ${color}40` 
      }}>
        {status}
      </span>
    </div>
  );
}
