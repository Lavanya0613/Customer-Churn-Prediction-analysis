import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { AlertCircle } from 'lucide-react';

export default function HighRiskTable() {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const res = await axios.get(`${apiUrl}/predictions/high-risk?limit=20`);
        setPredictions(res.data);
      } catch (err) {
        setError("Failed to load high-risk customers. Ensure the API is running and predictions have been saved.");
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', padding: '4rem' }}>
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '1200px' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', margin: '0 0 0.5rem 0' }}>High-Risk Customers</h1>
        <p style={{ color: 'var(--text-secondary)' }}>
          Review customers recently scored as High or Critical risk.
        </p>
      </header>
      
      {error && (
        <div style={{ padding: '1rem', background: 'var(--danger-bg)', border: '1px solid var(--danger)', borderRadius: 'var(--radius)', color: 'var(--danger)', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <AlertCircle size={20} />
          {error}
        </div>
      )}

      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Customer ID</th>
                <th>Probability</th>
                <th>Risk Level</th>
                <th>Retention Priority</th>
                <th>Top Risk Factor</th>
                <th>Recommended Action</th>
              </tr>
            </thead>
            <tbody>
              {predictions.length === 0 ? (
                <tr>
                  <td colSpan="6" style={{ textAlign: 'center', padding: '4rem 2rem', color: 'var(--text-secondary)' }}>
                    No high-risk predictions found in the database.
                  </td>
                </tr>
              ) : (
                predictions.map((p, idx) => (
                  <tr key={idx}>
                    <td style={{ fontWeight: 500, color: 'var(--text-primary)' }}>{p.customer_id}</td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <div style={{ width: '40px', background: 'rgba(255,255,255,0.1)', height: '4px', borderRadius: '2px', overflow: 'hidden' }}>
                          <div style={{ height: '100%', width: `${p.churn_probability * 100}%`, background: p.risk_level === 'Critical Risk' ? 'var(--danger)' : 'var(--warning)' }}></div>
                        </div>
                        {(p.churn_probability * 100).toFixed(1)}%
                      </div>
                    </td>
                    <td>
                      <span className="badge" style={{ 
                        background: p.risk_level === 'Critical Risk' ? 'var(--danger-bg)' : 'var(--warning-bg)', 
                        color: p.risk_level === 'Critical Risk' ? 'var(--danger)' : 'var(--warning)',
                        border: `1px solid ${p.risk_level === 'Critical Risk' ? 'rgba(239, 68, 68, 0.2)' : 'rgba(245, 158, 11, 0.2)'}`
                      }}>
                        {p.risk_level}
                      </span>
                    </td>
                    <td>
                      <span className="badge" style={{
                        background: p.retention_priority === 'Priority Retention' ? 'var(--danger-bg)' : 'var(--primary-bg)',
                        color: p.retention_priority === 'Priority Retention' ? 'var(--danger)' : 'var(--primary)',
                      }}>
                        {p.retention_priority || 'Standard Retention'}
                      </span>
                    </td>
                    <td style={{ color: 'var(--danger)' }}>{formatFactor(p.top_risk_factor)}</td>
                    <td>{p.recommended_action}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function formatFactor(factorStr) {
  if (!factorStr || factorStr === "None") return "None";
  return factorStr.replace(/_/g, ' ').replace(' = ', ': ').replace(/\b\w/g, l => l.toUpperCase());
}
