import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const SegmentationPage = ({ data }) => {
  const scatterData = data?.segment_scatter || [];

  const COLORS = {
    'High-Flight-Risk': 'var(--danger)',
    'Uncommitted': 'var(--warning)',
    'Premium': 'var(--primary)',
    'Budget': 'var(--success)'
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title text-gradient">Customer Segmentation</h1>
        <p className="page-subtitle">Analyzing customer behavior clusters based on contract type and spending.</p>
      </div>

      <div className="card">
        <div className="card-header">
          Tenure vs Monthly Charges by Segment
        </div>
        <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
          Business Question: How does spending behavior differ across segments?
        </p>
        
        <div style={{ height: '400px', marginBottom: '1.5rem' }}>
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
              <XAxis type="number" dataKey="tenure_months" name="Tenure" unit=" mo" stroke="var(--text-secondary)" />
              <YAxis type="number" dataKey="monthly_charges" name="Monthly Charges" unit=" $" stroke="var(--text-secondary)" />
              <Tooltip 
                cursor={{ strokeDasharray: '3 3', stroke: 'var(--border)' }} 
                contentStyle={{ backgroundColor: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: '8px' }}
              />
              <Legend />
              
              {Object.keys(COLORS).map(segment => (
                <Scatter 
                  key={segment}
                  name={segment} 
                  data={scatterData.filter(d => d.segment === segment)} 
                  fill={COLORS[segment]} 
                />
              ))}
            </ScatterChart>
          </ResponsiveContainer>
        </div>

        <div style={{ padding: '1rem', background: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.2)', borderRadius: 'var(--radius-sm)' }}>
          <h4 style={{ color: 'var(--accent)', marginBottom: '0.25rem', fontSize: '0.9rem' }}>Key Observation</h4>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
            The <strong style={{ color: 'var(--text-primary)' }}>High-Flight-Risk</strong> segment is densely packed in the low-tenure, variable-spend area.
            <strong style={{ color: 'var(--text-primary)' }}> Premium Loyalists</strong> occupy the top right (high tenure, high spend) and drive the majority of long-term revenue.
          </p>
        </div>
      </div>
    </div>
  );
};

export default SegmentationPage;
