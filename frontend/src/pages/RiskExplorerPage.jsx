import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const RiskExplorerPage = ({ data }) => {
  const [highRiskCustomers, setHighRiskCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const distribution = data?.risk_distribution || [];
  const shapImportance = data?.shap_importance || [];

  useEffect(() => {
    const fetchHighRisk = async () => {
      try {
        const response = await axios.get(`${API_URL}/predictions/high-risk?limit=10`);
        setHighRiskCustomers(response.data);
      } catch (err) {
        console.error("Failed to load high risk customers", err);
      } finally {
        setLoading(false);
      }
    };
    fetchHighRisk();
  }, []);

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title text-gradient">Risk Explorer & XAI</h1>
        <p className="page-subtitle">Explainable AI (SHAP) and actionable high-risk customer lists.</p>
      </div>

      <div className="grid grid-cols-2 mb-8">
        {/* SHAP Global Importance */}
        <div className="card">
          <h2 className="card-header">Global Feature Importance (SHAP)</h2>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart layout="vertical" data={shapImportance} margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} stroke="var(--border)" />
                <XAxis type="number" hide />
                <YAxis dataKey="feature" type="category" axisLine={false} tickLine={false} width={120} tick={{fontSize: 12, fill: 'var(--text-secondary)'}} />
                <Tooltip 
                  formatter={(val) => [val.toFixed(3), 'Mean |SHAP|']} 
                  contentStyle={{ backgroundColor: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: '8px' }}
                  cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                />
                <Bar dataKey="importance" fill="var(--danger)" radius={[0, 4, 4, 0]} barSize={15} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Distribution */}
        <div className="card">
          <h2 className="card-header">Predicted Risk Distribution</h2>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={distribution} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border)" />
                <XAxis dataKey="x" tickFormatter={(v) => v.toFixed(1)} stroke="var(--text-secondary)" />
                <YAxis hide />
                <Tooltip 
                  formatter={(val) => [val.toFixed(2), 'Density']} 
                  labelFormatter={(v) => `Probability: ${v.toFixed(2)}`} 
                  contentStyle={{ backgroundColor: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: '8px' }}
                  cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                />
                <Bar dataKey="y" fill="var(--accent)" radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* High Risk Table */}
      <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
        <div style={{ padding: '1.75rem 1.75rem 0' }}>
          <h2 className="card-header" style={{ marginBottom: '1.25rem' }}>Actionable High-Risk Customers</h2>
        </div>
        
        {loading ? (
          <div style={{ padding: '2rem', display: 'flex', justifyContent: 'center' }}><div className="spinner"></div></div>
        ) : highRiskCustomers.length === 0 ? (
          <p style={{ padding: '2rem', color: 'var(--text-muted)' }}>No high risk customers found in the database.</p>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Customer ID</th>
                  <th>Risk Probability</th>
                  <th>Retention Priority</th>
                  <th>Top Risk Factor</th>
                  <th>Recommended Action</th>
                </tr>
              </thead>
              <tbody>
                {highRiskCustomers.map((c, i) => (
                  <tr key={i}>
                    <td style={{ fontWeight: 500 }}>{c.customer_id}</td>
                    <td>
                      <span className={`badge ${c.churn_probability > 0.6 ? 'badge-danger badge-pulse' : 'badge-warning'}`}>
                        {(c.churn_probability * 100).toFixed(1)}%
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${c.retention_priority === 'Priority Retention' ? 'badge-danger' : 'badge-primary'}`}>
                        {c.retention_priority || 'Standard Retention'}
                      </span>
                    </td>
                    <td style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{c.top_risk_factor}</td>
                    <td style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', fontWeight: 500 }}>{c.recommended_action}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default RiskExplorerPage;
