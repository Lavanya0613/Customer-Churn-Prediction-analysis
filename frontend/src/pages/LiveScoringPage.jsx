import React, { useState } from 'react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const LiveScoringPage = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Initial state representing a high-risk profile for demo purposes
  const [formData, setFormData] = useState({
    customerid: `LIVE-${Math.floor(Math.random() * 9000) + 1000}`,
    tenure_months: 2,
    contract: "Month-to-month",
    monthly_charges: 95.50,
    total_charges: 191.00,
    internet_service: "Fiber optic",
    payment_method: "Electronic check",
    senior_citizen: "Yes",
    dependents: "No",
    partner: "No",
    phone_service: "Yes",
    multiple_lines: "No",
    online_security: "No",
    online_backup: "No",
    device_protection: "No",
    tech_support: "No",
    streaming_tv: "Yes",
    streaming_movies: "Yes",
    paperless_billing: "Yes",
    gender: "Female",
    country: "United States",
    state: "California",
    city: "Los Angeles",
    zip_code: 90001,
    lat_long: "33.973616, -118.242766",
    latitude: 33.973616,
    longitude: -118.242766,
    cltv: 4500.0
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name.includes('charges') || name === 'tenure_months' || name === 'cltv' ? Number(value) : value
    }));
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Use ?save=true to ensure it shows up on the Risk Explorer page!
      const response = await axios.post(`${API_URL}/predict?save=true`, formData);
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError("Failed to score customer. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title text-gradient">Live Scoring Simulator</h1>
        <p className="page-subtitle">Input customer parameters to evaluate live churn risk via the ML API.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3" style={{ gap: '2rem', marginBottom: '2rem' }}>
        
        {/* Input Form */}
        <div className="card" style={{ gridColumn: 'span 2' }}>
          <h2 className="card-header">Customer Profile Input</h2>
          <form onSubmit={handlePredict}>
            <div className="grid grid-cols-2" style={{ gap: '1.5rem', marginBottom: '1.5rem' }}>
              
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>Customer ID</label>
                <input type="text" name="customerid" value={formData.customerid} onChange={handleInputChange} 
                  style={{ width: '100%', padding: '0.75rem', background: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)', color: 'var(--text-primary)', outline: 'none' }} />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>Tenure (Months)</label>
                <input type="number" name="tenure_months" value={formData.tenure_months} onChange={handleInputChange} 
                  style={{ width: '100%', padding: '0.75rem', background: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)', color: 'var(--text-primary)', outline: 'none' }} />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>Contract Type</label>
                <select name="contract" value={formData.contract} onChange={handleInputChange}
                  style={{ width: '100%', padding: '0.75rem', background: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)', color: 'var(--text-primary)', outline: 'none', appearance: 'none' }}>
                  <option value="Month-to-month">Month-to-month</option>
                  <option value="One year">One year</option>
                  <option value="Two year">Two year</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>Internet Service</label>
                <select name="internet_service" value={formData.internet_service} onChange={handleInputChange}
                  style={{ width: '100%', padding: '0.75rem', background: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)', color: 'var(--text-primary)', outline: 'none', appearance: 'none' }}>
                  <option value="Fiber optic">Fiber optic</option>
                  <option value="DSL">DSL</option>
                  <option value="No">No</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>Monthly Charges ($)</label>
                <input type="number" step="0.01" name="monthly_charges" value={formData.monthly_charges} onChange={handleInputChange} 
                  style={{ width: '100%', padding: '0.75rem', background: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)', color: 'var(--text-primary)', outline: 'none' }} />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>Total Charges ($)</label>
                <input type="number" step="0.01" name="total_charges" value={formData.total_charges} onChange={handleInputChange} 
                  style={{ width: '100%', padding: '0.75rem', background: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)', color: 'var(--text-primary)', outline: 'none' }} />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>Payment Method</label>
                <select name="payment_method" value={formData.payment_method} onChange={handleInputChange}
                  style={{ width: '100%', padding: '0.75rem', background: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)', color: 'var(--text-primary)', outline: 'none', appearance: 'none' }}>
                  <option value="Electronic check">Electronic check</option>
                  <option value="Mailed check">Mailed check</option>
                  <option value="Bank transfer (automatic)">Bank transfer</option>
                  <option value="Credit card (automatic)">Credit card</option>
                </select>
              </div>
              
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>Tech Support</label>
                <select name="tech_support" value={formData.tech_support} onChange={handleInputChange}
                  style={{ width: '100%', padding: '0.75rem', background: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)', color: 'var(--text-primary)', outline: 'none', appearance: 'none' }}>
                  <option value="No">No</option>
                  <option value="Yes">Yes</option>
                  <option value="No internet service">No internet service</option>
                </select>
              </div>

            </div>

            <button type="submit" disabled={loading} style={{ 
              width: '100%', 
              padding: '1rem', 
              background: 'linear-gradient(to right, var(--primary), #6366F1)', 
              color: 'white', 
              border: 'none', 
              borderRadius: 'var(--radius-sm)', 
              fontWeight: 600, 
              cursor: loading ? 'not-allowed' : 'pointer',
              opacity: loading ? 0.7 : 1,
              transition: 'all 0.2s ease'
            }}>
              {loading ? 'Scoring via API...' : 'Predict Churn Risk'}
            </button>
          </form>
        </div>

        {/* Results Panel */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          
          <div className="card" style={{ flex: 1 }}>
            <h2 className="card-header">Prediction Result</h2>
            
            {!result && !error && !loading && (
              <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)', fontSize: '0.9rem', textAlign: 'center', minHeight: '300px' }}>
                Fill out the customer profile and click predict to see the live score.
              </div>
            )}

            {loading && (
              <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '300px' }}>
                <div className="spinner"></div>
              </div>
            )}

            {error && (
              <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.2)', borderRadius: 'var(--radius-sm)', color: 'var(--danger)' }}>
                {error}
              </div>
            )}

            {result && !loading && (
              <div style={{ animation: 'fade-in 0.5s ease-out' }}>
                
                <div style={{ textAlign: 'center', padding: '2rem 0', borderBottom: '1px solid var(--border)', marginBottom: '1.5rem' }}>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Churn Probability</div>
                  <div style={{ fontSize: '3.5rem', fontWeight: 800, color: result.churn_probability > 0.6 ? 'var(--danger)' : (result.churn_probability > 0.2 ? 'var(--warning)' : 'var(--success)'), lineHeight: 1 }}>
                    {(result.churn_probability * 100).toFixed(1)}%
                  </div>
                  <div style={{ marginTop: '1rem' }}>
                    <span className={`badge ${result.risk_level.includes('High') || result.risk_level.includes('Critical') ? 'badge-danger badge-pulse' : 'badge-primary'}`}>
                      {result.risk_level}
                    </span>
                  </div>
                </div>

                <div style={{ marginBottom: '1.5rem' }}>
                  <h4 style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.25rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Retention Priority</h4>
                  <div style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-primary)' }}>{result.retention_priority}</div>
                </div>

                <div style={{ marginBottom: '1.5rem' }}>
                  <h4 style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.25rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Top Risk Factor</h4>
                  <div style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>{result.top_risk_factor}</div>
                </div>

                <div style={{ padding: '1rem', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.2)', borderRadius: 'var(--radius-sm)' }}>
                  <h4 style={{ color: 'var(--success)', marginBottom: '0.25rem', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Recommended Action</h4>
                  <p style={{ color: 'var(--text-primary)', fontSize: '0.95rem', fontWeight: 500 }}>
                    {result.recommended_action}
                  </p>
                </div>

              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
};

export default LiveScoringPage;
