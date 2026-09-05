import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { LayoutDashboard, PieChart, Users, Activity, Target, Zap } from 'lucide-react';

const DashboardLayout = () => {
  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <Target size={28} className="text-accent" />
          <span className="text-gradient-primary">ChurnAI</span>
        </div>
        
        <nav className="sidebar-nav">
          <NavItem to="/" icon={<LayoutDashboard size={20} />} label="Executive Overview" />
          <NavItem to="/eda" icon={<PieChart size={20} />} label="Churn Drivers" />
          <NavItem to="/segmentation" icon={<Users size={20} />} label="Segmentation" />
          <NavItem to="/ml-performance" icon={<Activity size={20} />} label="ML Performance" />
          <NavItem to="/risk-explorer" icon={<Target size={20} />} label="Risk Explorer" />
          <NavItem to="/live-scoring" icon={<Zap size={20} />} label="Live Scoring" />
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
          <Outlet />
        </div>
      </main>
    </div>
  );
};

const NavItem = ({ to, icon, label }) => {
  return (
    <NavLink
      to={to}
      className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
    >
      {icon}
      <span>{label}</span>
    </NavLink>
  );
};

export default DashboardLayout;
