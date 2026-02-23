import { Link } from "react-router-dom";
import { useContext, useEffect, useState } from "react";
import { ThemeContext } from "../context/ThemeContext";
import "./Home.css";

function Home() {
  const { theme, toggleTheme } = useContext(ThemeContext);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div className="home-container">
      <nav className={`home-nav ${scrolled ? 'scrolled' : ''}`}>
        <div className="nav-content">
          <div className="nav-logo">
            <div className="logo-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
              </svg>
            </div>
            <span className="logo-text">MediCare <span className="logo-accent">CDSS</span></span>
          </div>
          <div className="nav-actions">
            <button className="btn-theme" onClick={toggleTheme} title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}>
              {theme === "light" ? (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                </svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="5"/>
                  <line x1="12" y1="1" x2="12" y2="3"/>
                  <line x1="12" y1="21" x2="12" y2="23"/>
                  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                  <line x1="1" y1="12" x2="3" y2="12"/>
                  <line x1="21" y1="12" x2="23" y2="12"/>
                  <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
                </svg>
              )}
            </button>
            <Link to="/login" className="btn-nav-secondary">Sign In</Link>
            <Link to="/register" className="btn-nav-primary">Get Started</Link>
          </div>
        </div>
      </nav>

      <section className="hero-section">
        <div className="hero-background">
          <div className="gradient-orb orb-1"></div>
          <div className="gradient-orb orb-2"></div>
          <div className="gradient-orb orb-3"></div>
          <div className="grid-pattern"></div>
        </div>

        <div className="hero-content">
          <div className="hero-badge animate-fade-in">
            <span className="badge-dot"></span>
            <span>AI-Powered Medical Intelligence</span>
          </div>
          
          <h1 className="hero-title animate-slide-up">
            Transform Medical Data Into
            <span className="gradient-text"> Actionable Insights</span>
          </h1>
          
          <p className="hero-description animate-slide-up delay-1">
            Advanced hybrid AI system combining cutting-edge machine learning with clinical expertise
            for precise medical test analysis and comprehensive risk assessment.
          </p>
          
          <div className="hero-actions animate-slide-up delay-2">
            <Link to="/register" className="btn-hero-primary">
              <span>Start Free Analysis</span>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="5" y1="12" x2="19" y2="12"/>
                <polyline points="12 5 19 12 12 19"/>
              </svg>
            </Link>
            <Link to="/login" className="btn-hero-secondary">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <polygon points="10 8 16 12 10 16 10 8"/>
              </svg>
              <span>Watch Demo</span>
            </Link>
          </div>

          <div className="hero-stats animate-fade-in delay-3">
            <div className="stat-item">
              <div className="stat-number">10K+</div>
              <div className="stat-label">Analyses Done</div>
            </div>
            <div className="stat-divider"></div>
            <div className="stat-item">
              <div className="stat-number">24/7</div>
              <div className="stat-label">Availability</div>
            </div>
            <div className="stat-divider"></div>
            <div className="stat-item">
              <div className="stat-number">3</div>
              <div className="stat-label">Health Panels</div>
            </div>
          </div>
        </div>

        <div className="hero-visual animate-fade-in delay-2">
          <div className="dashboard-preview">
            <div className="preview-header">
              <div className="preview-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <div className="preview-title">Medical Dashboard</div>
            </div>
            <div className="preview-content">
              <div className="preview-card card-pulse">
                <div className="card-icon icon-success">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="20 6 9 17 4 12"/>
                  </svg>
                </div>
                <div className="card-text">
                  <div className="card-label">Analysis Complete</div>
                  <div className="card-value">Normal Range</div>
                </div>
              </div>
              <div className="preview-card card-pulse delay-1">
                <div className="card-icon icon-warning">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                    <line x1="12" y1="9" x2="12" y2="13"/>
                    <line x1="12" y1="17" x2="12.01" y2="17"/>
                  </svg>
                </div>
                <div className="card-text">
                  <div className="card-label">Risk Assessment</div>
                  <div className="card-value">Moderate Risk</div>
                </div>
              </div>
              <div className="preview-card card-pulse delay-2">
                <div className="card-icon icon-info">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="16" x2="12" y2="12"/>
                    <line x1="12" y1="8" x2="12.01" y2="8"/>
                  </svg>
                </div>
                <div className="card-text">
                  <div className="card-label">AI Recommendation</div>
                  <div className="card-value">Follow-up in 3 months</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="features-section">
        <div className="section-header animate-on-scroll">
          <div className="section-badge">
            <span>Comprehensive Analysis</span>
          </div>
          <h2>Advanced Medical Intelligence</h2>
          <p>Powered by hybrid AI combining machine learning with clinical guidelines</p>
        </div>

        <div className="features-grid">
          <div className="feature-card animate-on-scroll">
            <div className="feature-icon-wrapper">
              <div className="feature-icon diabetes">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
              </div>
              <div className="icon-glow diabetes-glow"></div>
            </div>
            <h3>Diabetes Panel</h3>
            <p>Comprehensive analysis of HbA1c, FBS, and PPBS with AI-powered risk stratification and personalized lifestyle recommendations.</p>
            <div className="feature-tags">
              <span>HbA1c</span>
              <span>FBS</span>
              <span>PPBS</span>
            </div>
          </div>

          <div className="feature-card animate-on-scroll delay-1">
            <div className="feature-icon-wrapper">
              <div className="feature-icon cardio">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
              </div>
              <div className="icon-glow cardio-glow"></div>
            </div>
            <h3>Cardiovascular Panel</h3>
            <p>Advanced heart health assessment analyzing blood pressure, cholesterol levels, and cardiac markers with preventive care insights.</p>
            <div className="feature-tags">
              <span>BP</span>
              <span>Cholesterol</span>
              <span>Cardiac</span>
            </div>
          </div>

          <div className="feature-card animate-on-scroll delay-2">
            <div className="feature-icon-wrapper">
              <div className="feature-icon kidney">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                </svg>
              </div>
              <div className="icon-glow kidney-glow"></div>
            </div>
            <h3>Kidney Function Panel</h3>
            <p>Precise kidney health evaluation through creatinine and BUN analysis for early detection of renal dysfunction and disease.</p>
            <div className="feature-tags">
              <span>Creatinine</span>
              <span>BUN</span>
              <span>GFR</span>
            </div>
          </div>
        </div>
      </section>

      <section className="how-it-works-section">
        <div className="section-header animate-on-scroll">
          <div className="section-badge">
            <span>Simple Process</span>
          </div>
          <h2>How It Works</h2>
          <p>Get started in three simple steps</p>
        </div>

        <div className="steps-container">
          <div className="step-item animate-on-scroll">
            <div className="step-number">01</div>
            <div className="step-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
            </div>
            <h3>Upload Report</h3>
            <p>Simply upload your medical lab report in PDF format</p>
          </div>

          <div className="step-connector animate-on-scroll delay-1"></div>

          <div className="step-item animate-on-scroll delay-1">
            <div className="step-number">02</div>
            <div className="step-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>
            <h3>AI Analysis</h3>
            <p>Our hybrid AI system analyzes your data in seconds</p>
          </div>

          <div className="step-connector animate-on-scroll delay-2"></div>

          <div className="step-item animate-on-scroll delay-2">
            <div className="step-number">03</div>
            <div className="step-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
              </svg>
            </div>
            <h3>Get Insights</h3>
            <p>Receive detailed analysis and personalized recommendations</p>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="cta-background">
          <div className="cta-orb cta-orb-1"></div>
          <div className="cta-orb cta-orb-2"></div>
        </div>
        <div className="cta-content animate-on-scroll">
          <h2>Ready to Transform Your Healthcare?</h2>
          <p>Join thousands of healthcare professionals using AI-powered clinical decision support</p>
          <Link to="/register" className="btn-cta">
            <span>Create Free Account</span>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12 5 19 12 12 19"/>
            </svg>
          </Link>
          <p className="cta-note">No credit card required • Free forever</p>
        </div>
      </section>

      <footer className="home-footer">
        <div className="footer-content">
          <div className="footer-brand">
            <div className="footer-logo">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
              </svg>
              <span>MediCare CDSS</span>
            </div>
            <p>Advanced AI-powered clinical decision support for modern healthcare.</p>
          </div>
          <div className="footer-links">
            <div className="footer-column">
              <h4>Product</h4>
              <Link to="/register">Get Started</Link>
              <Link to="/login">Sign In</Link>
            </div>
            <div className="footer-column">
              <h4>Company</h4>
              <a href="#">About Us</a>
              <a href="#">Contact</a>
            </div>
            <div className="footer-column">
              <h4>Legal</h4>
              <a href="#">Privacy Policy</a>
              <a href="#">Terms of Service</a>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2024 MediCare CDSS. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default Home;
