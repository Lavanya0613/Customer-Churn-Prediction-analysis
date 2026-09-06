import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const OverviewPage = ({ data }) => {
  const kpis = data?.kpis || {};
  const contractData = data?.churn_by_contract || [];

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title text-gradient">Executive Overview</h1>
        <p className="page-subtitle">High-level KPIs and business metrics for customer retention.</p>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-3 mb-8">
        <KpiCard 
          title="Total Customers" 
          value={kpis.total_customers?.toLocaleString() || '0'} 
          subtitle="Analyzed in dataset"
        />
        <KpiCard 
          title="Global Churn Rate" 
          value={`${((kpis.churn_rate || 0) * 100).toFixed(1)}%`} 
          subtitle="Target threshold: 20%"
        />
        <KpiCard 
          title="Avg. Monthly Revenue" 
          value={`$${(kpis.avg_mrr || 0).toFixed(2)}`} 
          subtitle="Per customer"
        />
      </div>

      <div className="card" style={{ marginBottom: '2rem' }}>
        <h2 className="card-header">About ChurnAI</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', color: 'var(--text-secondary)' }}>
          <p>
            <strong style={{ color: 'var(--text-primary)' }}>What is this project?</strong> ChurnAI is a machine-learning-powered platform designed to identify high-risk telecommunications customers before they cancel their service.
          </p>
          <p>
            <strong style={{ color: 'var(--text-primary)' }}>What does it do?</strong> It uses a Logistic Regression model to score customers in real-time, assigning a churn probability and generating actionable, business-driven retention recommendations (e.g. offering annual discounts to month-to-month users). It also utilizes SHAP Explainable AI to tell you exactly <em>why</em> a customer is predicted to churn.
          </p>
          <p>
            <strong style={{ color: 'var(--text-primary)' }}>How does it solve the problem?</strong> By automatically surfacing highly probable churners and providing specific, interpretative intervention strategies, it transforms raw data into a targeted "hit list" for retention teams, maximizing customer lifetime value and reducing lost revenue.
          </p>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          Churn Rate by Contract Type
        </div>
        <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
          Business Question: Which contracts suffer the most churn?
        </p>
        
        <div style={{ height: '320px', marginBottom: '1.5rem' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={contractData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border)" />
              <XAxis dataKey="contract" axisLine={false} tickLine={false} stroke="var(--text-secondary)" />
              <YAxis 
                tickFormatter={(tick) => `${(tick * 100).toFixed(0)}%`} 
                axisLine={false} 
                tickLine={false}
                stroke="var(--text-secondary)"
              />
              <Tooltip 
                formatter={(value) => [`${(value * 100).toFixed(1)}%`, 'Churn Rate']}
                contentStyle={{ backgroundColor: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: '8px' }}
                cursor={{ fill: 'rgba(255,255,255,0.05)' }}
              />
              <Bar dataKey="rate" fill="var(--accent)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div style={{ padding: '1rem', background: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.2)', borderRadius: 'var(--radius-sm)' }}>
          <h4 style={{ color: 'var(--accent)', marginBottom: '0.25rem', fontSize: '0.9rem' }}>Key Observation</h4>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
            Month-to-month contracts have a significantly higher churn rate compared to 1-year or 2-year contracts. 
            Customers without long-term commitments represent the highest flight risk.
          </p>
        </div>
      </div>
    </div>
  );
};

const KpiCard = ({ title, value, subtitle }) => (
  <div className="card metric-card">
    <h3 className="metric-title">{title}</h3>
    <p className="metric-value">{value}</p>
    <p className="metric-subtext">{subtitle}</p>
  </div>
);

export default OverviewPage;
