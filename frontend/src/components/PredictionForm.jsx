import React, { useState } from 'react';
import axios from 'axios';
import { AlertCircle, Target, ShieldCheck, Activity } from 'lucide-react';

export default function PredictionForm() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  
  // Default values based on our Pydantic schema
  const [formData, setFormData] = useState({
    customerid: "NEW-" + Math.floor(Math.random() * 10000),
    tenure_months: 12,
    contract: "Month-to-month",
    monthly_charges: 70.0,
    total_charges: 840.0,
    cltv: 5000.0,
    internet_service: "Fiber optic",
    tech_support: "No",
    online_security: "No",
    payment_method: "Electronic check",
    paperless_billing: "Yes",
    country: "United States",
    state: "California",
    city: "Los Angeles",
    zip_code: 90001,
    lat_long: "33.973616, -118.242766",
    latitude: 33.973616,
    longitude: -118.242766,
    gender: "Male",
    senior_citizen: "No",
    partner: "No",
    dependents: "No",
    phone_service: "Yes",
    multiple_lines: "No",
    online_backup: "No",
    device_protection: "No",
    streaming_tv: "No",
    streaming_movies: "No"
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    // Handle number conversions for specific fields
    const isNum = ['tenure_months', 'monthly_charges', 'total_charges', 'cltv', 'zip_code', 'latitude', 'longitude'].includes(name);
    setFormData(prev => ({
      ...prev,
      [name]: isNum ? Number(value) : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await axios.post(`${apiUrl}/predict?save=true`, formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred while connecting to the prediction service.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1000px' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', margin: '0 0 0.5rem 0' }}>Score Customer Risk</h1>
        <p style={{ color: 'var(--text-secondary)' }}>
          Enter customer attributes to generate real-time churn probability, SHAP factors, and recommendations.
        </p>
      </header>

      <div className="grid grid-cols-1" style={{ gap: '2rem' }}>
        
        {/* Input Form */}
        <div className="card">
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-3" style={{ marginBottom: '1.5rem' }}>
              
              <div className="form-group">
                <label className="form-label">Customer ID</label>
                <input 
                  type="text" name="customerid" className="form-input" 
                  value={formData.customerid} onChange={handleChange} required 
                />
              </div>

              <div className="form-group">
                <label className="form-label">Tenure (Months)</label>
                <input 
                  type="number" name="tenure_months" className="form-input" 
                  value={formData.tenure_months} onChange={handleChange} required min="0" 
                />
              </div>

              <div className="form-group">
                <label className="form-label">Contract Type</label>
                <select name="contract" className="form-select" value={formData.contract} onChange={handleChange}>
                  <option value="Month-to-month">Month-to-month</option>
                  <option value="One year">One year</option>
                  <option value="Two year">Two year</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Monthly Charges ($)</label>
                <input 
                  type="number" name="monthly_charges" step="0.01" className="form-input" 
                  value={formData.monthly_charges} onChange={handleChange} required 
                />
              </div>
              
              <div className="form-group">
                <label className="form-label">Total Charges ($)</label>
                <input 
                  type="number" name="total_charges" step="0.01" className="form-input" 
                  value={formData.total_charges} onChange={handleChange} required 
                />
              </div>

              <div className="form-group">
                <label className="form-label">Internet Service</label>
                <select name="internet_service" className="form-select" value={formData.internet_service} onChange={handleChange}>
                  <option value="DSL">DSL</option>
                  <option value="Fiber optic">Fiber optic</option>
                  <option value="No">No</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Tech Support</label>
                <select name="tech_support" className="form-select" value={formData.tech_support} onChange={handleChange}>
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                  <option value="No internet service">No internet service</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Online Security</label>
                <select name="online_security" className="form-select" value={formData.online_security} onChange={handleChange}>
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                  <option value="No internet service">No internet service</option>
                </select>
              </div>
              
              <div className="form-group">
                <label className="form-label">Payment Method</label>
                <select name="payment_method" className="form-select" value={formData.payment_method} onChange={handleChange}>
                  <option value="Electronic check">Electronic check</option>
                  <option value="Mailed check">Mailed check</option>
                  <option value="Bank transfer (automatic)">Bank transfer (automatic)</option>
                  <option value="Credit card (automatic)">Credit card (automatic)</option>
                </select>
              </div>

            </div>
            
            <div style={{ display: 'flex', justifyContent: 'flex-end', borderTop: '1px solid var(--border)', paddingTop: '1.5rem' }}>
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? <div className="spinner" style={{ width: '16px', height: '16px', borderWidth: '2px' }}/> : <Activity size={18} />}
                Generate Intelligence
              </button>
            </div>
          </form>
        </div>

        {/* Results Area */}
        {error && (
          <div style={{ padding: '1rem', background: 'var(--danger-bg)', border: '1px solid var(--danger)', borderRadius: 'var(--radius)', color: 'var(--danger)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <AlertCircle size={20} />
            {error}
          </div>
        )}

        {result && (
          <div className="card" style={{ borderLeft: `4px solid ${getRiskColor(result.risk_level)}` }}>
            <h3 style={{ marginBottom: '1.5rem', fontSize: '1.25rem' }}>Prediction Results</h3>
            
            <div className="grid grid-cols-2" style={{ gap: '2rem' }}>
              <div>
                <div style={{ marginBottom: '1.5rem' }}>
                  <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Churn Probability</div>
                  <div style={{ fontSize: '2.5rem', fontWeight: 700, color: getRiskColor(result.risk_level), lineHeight: 1 }}>
                    {(result.churn_probability * 100).toFixed(1)}%
                  </div>
                  <div style={{ marginTop: '0.5rem' }}>
                    <span className={`badge`} style={{ background: `${getRiskColor(result.risk_level)}20`, color: getRiskColor(result.risk_level) }}>
                      {result.risk_level}
                    </span>
                  </div>
                </div>

                <div>
                  <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Recommended Action</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 500, color: 'var(--text-primary)' }}>
                    {result.recommended_action}
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', background: 'rgba(0,0,0,0.2)', padding: '1.5rem', borderRadius: 'var(--radius)' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--danger)', marginBottom: '0.25rem', fontSize: '0.875rem', fontWeight: 600, textTransform: 'uppercase' }}>
                    <Target size={16} /> Top Risk Factor
                  </div>
                  <div style={{ color: 'var(--text-primary)' }}>{formatFactor(result.top_risk_factor)}</div>
                </div>
                
                <div style={{ borderTop: '1px solid var(--border)', paddingTop: '1rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--success)', marginBottom: '0.25rem', fontSize: '0.875rem', fontWeight: 600, textTransform: 'uppercase' }}>
                    <ShieldCheck size={16} /> Protective Factor
                  </div>
                  <div style={{ color: 'var(--text-primary)' }}>{formatFactor(result.protective_factors)}</div>
                </div>
              </div>
            </div>
          </div>
        )}
        
      </div>
    </div>
  );
}

function getRiskColor(riskLevel) {
  if (riskLevel === "Critical Risk") return "var(--danger)";
  if (riskLevel === "High Risk") return "var(--warning)";
  return "var(--success)";
}

function formatFactor(factorStr) {
  if (!factorStr || factorStr === "None") return "None identified";
  // Convert "tenure_months = 12" to "Tenure Months (12)" for better readability
  return factorStr.replace(/_/g, ' ').replace(' = ', ': ').replace(/\b\w/g, l => l.toUpperCase());
}
