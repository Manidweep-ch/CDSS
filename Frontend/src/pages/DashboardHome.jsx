import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import DashboardLayout from "../components/DashboardLayout";
import axiosClient from "../api/axiosClient";
import "./DashboardHome.css";

function DashboardHome() {
  const [stats, setStats] = useState({
    totalProfiles: 0,
    totalEvaluations: 0,
    recentEvaluations: []
  });

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const profilesRes = await axiosClient.get("/profiles/");
      const profiles = profilesRes.data;
      
      let totalEvals = 0;
      let allEvaluations = [];
      
      for (const profile of profiles) {
        try {
          const historyRes = await axiosClient.get(`/evaluate/history/${profile.id}`);
          totalEvals += historyRes.data.length;
          allEvaluations = [...allEvaluations, ...historyRes.data.map(e => ({
            ...e,
            profileName: profile.profile_name
          }))];
        } catch (err) {
          console.error(`Failed to fetch history for profile ${profile.id}`);
        }
      }
      
      allEvaluations.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
      
      setStats({
        totalProfiles: profiles.length,
        totalEvaluations: totalEvals,
        recentEvaluations: allEvaluations.slice(0, 5)
      });
    } catch (err) {
      console.error("Failed to fetch dashboard data:", err);
    }
  };

  return (
    <DashboardLayout>
      <div className="dashboard-home fade-in">
        <div className="welcome-section">
          <div className="welcome-content">
            <h1 className="welcome-title">
              Welcome to <span className="gradient-text">MediCare CDSS</span>
            </h1>
            <p className="welcome-subtitle">
              Your intelligent clinical decision support system powered by advanced AI
            </p>
          </div>
          <div className="welcome-illustration">
            <div className="illustration-card card-float">
              <div className="card-icon gradient-blue">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                </svg>
              </div>
              <div className="card-label">AI Analysis</div>
            </div>
            <div className="illustration-card card-float delay-1">
              <div className="card-icon gradient-purple">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                </svg>
              </div>
              <div className="card-label">Reports</div>
            </div>
            <div className="illustration-card card-float delay-2">
              <div className="card-icon gradient-green">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              </div>
              <div className="card-label">Insights</div>
            </div>
          </div>
        </div>

        <div className="stats-grid">
          <div className="stat-card gradient-card-blue">
            <div className="stat-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <div className="stat-content">
              <div className="stat-value">{stats.totalProfiles}</div>
              <div className="stat-label">Patient Profiles</div>
            </div>
            <Link to="/dashboard/profiles" className="stat-link">
              Manage Profiles
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="5" y1="12" x2="19" y2="12"/>
                <polyline points="12 5 19 12 12 19"/>
              </svg>
            </Link>
          </div>

          <div className="stat-card gradient-card-purple">
            <div className="stat-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
              </svg>
            </div>
            <div className="stat-content">
              <div className="stat-value">{stats.totalEvaluations}</div>
              <div className="stat-label">Total Analyses</div>
            </div>
            <Link to="/dashboard/history" className="stat-link">
              View History
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="5" y1="12" x2="19" y2="12"/>
                <polyline points="12 5 19 12 12 19"/>
              </svg>
            </Link>
          </div>

          <div className="stat-card gradient-card-green">
            <div className="stat-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M9 11l3 3L22 4"/>
                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
              </svg>
            </div>
            <div className="stat-content">
              <div className="stat-value">3</div>
              <div className="stat-label">Health Panels</div>
            </div>
            <Link to="/dashboard/analyze" className="stat-link">
              Start Analysis
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="5" y1="12" x2="19" y2="12"/>
                <polyline points="12 5 19 12 12 19"/>
              </svg>
            </Link>
          </div>
        </div>

        <div className="quick-actions-section">
          <h2>Quick Actions</h2>
          <div className="actions-grid">
            <Link to="/dashboard/profiles" className="action-card gradient-border-blue">
              <div className="action-icon gradient-blue">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="8.5" cy="7" r="4"/>
                  <line x1="20" y1="8" x2="20" y2="14"/>
                  <line x1="23" y1="11" x2="17" y2="11"/>
                </svg>
              </div>
              <h3>Create Profile</h3>
              <p>Add a new patient profile to get started</p>
            </Link>

            <Link to="/dashboard/analyze" className="action-card gradient-border-purple">
              <div className="action-icon gradient-purple">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
              </div>
              <h3>Upload Report</h3>
              <p>Upload a lab report for AI analysis</p>
            </Link>

            <Link to="/dashboard/history" className="action-card gradient-border-green">
              <div className="action-icon gradient-green">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
              </div>
              <h3>View History</h3>
              <p>Access past evaluations and reports</p>
            </Link>
          </div>
        </div>

        {stats.recentEvaluations.length > 0 && (
          <div className="recent-section">
            <div className="section-header">
              <h2>Recent Evaluations</h2>
              <Link to="/dashboard/history" className="view-all-link">
                View All
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="5" y1="12" x2="19" y2="12"/>
                  <polyline points="12 5 19 12 12 19"/>
                </svg>
              </Link>
            </div>
            <div className="recent-list">
              {stats.recentEvaluations.map((evaluation) => (
                <Link 
                  key={evaluation.id} 
                  to={`/dashboard/view/${evaluation.id}`}
                  className="recent-item"
                >
                  <div className="recent-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                    </svg>
                  </div>
                  <div className="recent-content">
                    <div className="recent-title">{evaluation.profileName}</div>
                    <div className="recent-meta">
                      {evaluation.panels_run?.join(", ")} • {new Date(evaluation.timestamp).toLocaleDateString()}
                    </div>
                  </div>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="9 18 15 12 9 6"/>
                  </svg>
                </Link>
              ))}
            </div>
          </div>
        )}

        <div className="features-overview">
          <h2>What We Analyze</h2>
          <div className="features-grid">
            <div className="feature-item">
              <div className="feature-icon-wrapper gradient-blue">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
              </div>
              <h3>Diabetes Panel</h3>
              <p>HbA1c, FBS, PPBS analysis with risk assessment</p>
            </div>
            <div className="feature-item">
              <div className="feature-icon-wrapper gradient-purple">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
              </div>
              <h3>Cardiovascular</h3>
              <p>Heart health and blood pressure monitoring</p>
            </div>
            <div className="feature-item">
              <div className="feature-icon-wrapper gradient-green">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                </svg>
              </div>
              <h3>Kidney Function</h3>
              <p>Creatinine and BUN evaluation</p>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default DashboardHome;
