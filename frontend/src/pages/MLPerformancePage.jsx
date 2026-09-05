import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const MLPerformancePage = ({ data }) => {
  const tradeoff = data?.threshold_tradeoff || [];
  const metrics = data?.model_metrics || [];

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title text-gradient">Machine Learning Performance</h1>
        <p className="page-subtitle">Evaluating model accuracy and business cost thresholds.</p>
      </div>

      {/* Model Benchmark Table */}
      <div className="card" style={{ marginBottom: '2rem', padding: '0', overflow: 'hidden' }}>
        <div style={{ padding: '1.75rem 1.75rem 0' }}>
          <h2 className="card-header" style={{ marginBottom: '1.25rem' }}>Model Benchmark (Test Set)</h2>
        </div>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Model</th>
                <th>ROC-AUC</th>
                <th>PR-AUC</th>
              </tr>
            </thead>
            <tbody>
              {metrics.map((m, i) => (
                <tr key={i} style={m.name === 'Logistic Regression' ? { background: 'rgba(59, 130, 246, 0.05)' } : {}}>
                  <td style={{ fontWeight: 500 }}>
                    {m.name} {m.name === 'Logistic Regression' && <span className="badge badge-primary" style={{ marginLeft: '0.5rem' }}>Selected</span>}
                  </td>
                  <td style={{ color: 'var(--text-secondary)' }}>{m.roc_auc.toFixed(3)}</td>
                  <td style={{ color: 'var(--text-secondary)' }}>{m.pr_auc.toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          Threshold Optimization (Cost Matrix)
        </div>
        <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
          Business Question: At what probability threshold is Net Business Value maximized?
        </p>
        
        <div style={{ height: '320px', marginBottom: '1.5rem' }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={tradeoff} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border)" />
              <XAxis dataKey="threshold" name="Threshold" type="number" tickFormatter={(v) => v.toFixed(2)} stroke="var(--text-secondary)" />
              <YAxis yAxisId="left" tickFormatter={(val) => `${(val * 100).toFixed(0)}%`} stroke="var(--text-secondary)" />
              <YAxis yAxisId="right" orientation="right" tickFormatter={(val) => `$${val}`} stroke="var(--text-secondary)" />
              <Tooltip 
                formatter={(value, name) => [
                  name === 'net_value' ? `$${value.toFixed(0)}` : `${(value * 100).toFixed(1)}%`, 
                  name === 'net_value' ? 'Net Business Value' : name
                ]} 
                contentStyle={{ backgroundColor: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: '8px' }}
              />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="precision" stroke="var(--primary)" strokeWidth={2} dot={false} name="Precision" />
              <Line yAxisId="left" type="monotone" dataKey="recall" stroke="var(--warning)" strokeWidth={2} dot={false} name="Recall" />
              <Line yAxisId="right" type="monotone" dataKey="net_value" stroke="var(--success)" strokeWidth={3} dot={false} name="Net Value ($)" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={{ padding: '1rem', background: 'rgba(139, 92, 246, 0.1)', border: '1px solid rgba(139, 92, 246, 0.2)', borderRadius: 'var(--radius-sm)' }}>
          <h4 style={{ color: 'var(--primary)', marginBottom: '0.25rem', fontSize: '0.9rem' }}>Business Interpretation</h4>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
            Assuming a $100 value for retaining a True Positive and a $20 cost for a False Positive promotion, 
            the Net Business Value peaks at a classification threshold of <strong style={{ color: 'var(--text-primary)' }}>0.20</strong>. 
            Defaulting to 0.50 (highest accuracy) leaves significant revenue on the table.
          </p>
        </div>
      </div>
    </div>
  );
};

export default MLPerformancePage;
