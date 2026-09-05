import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const EDAPage = ({ data }) => {
  const tenureChurned = data?.tenure_dist_churned || [];
  const tenureRetained = data?.tenure_dist_retained || [];

  // Combine KDE data for tenure
  const tenureDataMap = {};
  tenureChurned.forEach(d => { tenureDataMap[Math.round(d.x)] = { x: Math.round(d.x), churned: d.y }; });
  tenureRetained.forEach(d => { 
    const key = Math.round(d.x);
    if (!tenureDataMap[key]) tenureDataMap[key] = { x: key };
    tenureDataMap[key].retained = d.y; 
  });
  const combinedTenure = Object.values(tenureDataMap).sort((a, b) => a.x - b.x);

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title text-gradient">Churn Drivers (EDA)</h1>
        <p className="page-subtitle">Investigating the factors that influence customer churn.</p>
      </div>

      <div className="card">
        <div className="card-header">
          Tenure Distribution by Churn Status
        </div>
        <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
          Business Question: Does tenure differ between churned and retained customers?
        </p>
        
        <div style={{ height: '320px', marginBottom: '1.5rem' }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={combinedTenure} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border)" />
              <XAxis dataKey="x" name="Tenure (Months)" tick={{fill: 'var(--text-secondary)'}} stroke="var(--text-secondary)" />
              <YAxis tickFormatter={(val) => val.toFixed(3)} tick={{fill: 'var(--text-secondary)'}} stroke="var(--text-secondary)" />
              <Tooltip 
                labelFormatter={(label) => `Tenure: ${label} months`}
                formatter={(value, name) => [value.toFixed(4), name === 'churned' ? 'Churned (Density)' : 'Retained (Density)']}
                contentStyle={{ backgroundColor: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: '8px' }}
              />
              <Legend />
              <Line type="monotone" dataKey="churned" stroke="var(--danger)" strokeWidth={2} dot={false} name="Churned" />
              <Line type="monotone" dataKey="retained" stroke="var(--success)" strokeWidth={2} dot={false} name="Retained" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={{ padding: '1rem', background: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.2)', borderRadius: 'var(--radius-sm)' }}>
          <h4 style={{ color: 'var(--accent)', marginBottom: '0.25rem', fontSize: '0.9rem' }}>Key Observation</h4>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
            Churned customers have a heavily right-skewed distribution, indicating that the majority of churn happens very early in the customer lifecycle (months 1-5). 
            Retained customers are uniformly distributed, with a spike at high tenure (70+ months) representing loyal long-term customers.
          </p>
        </div>
      </div>
    </div>
  );
};

export default EDAPage;
