import React, { useState, useEffect } from 'react';
import LandingPage from './components/LandingPage';
import ResearchForm from './components/ResearchForm';
import ApprovalPanel from './components/ApprovalPanel';
import ProgressPanel from './components/ProgressPanel';
import ReportPanel from './components/ReportPanel';
import { API_BASE } from './config';

function App() {
  const [view, setView] = useState('landing'); // 'landing' | 'app'
  const [runId, setRunId] = useState(null);
  const [status, setStatus] = useState("idle");
  const [plan, setPlan] = useState([]);
  
  useEffect(() => {
    if (runId && status === "idle") {
      const timer = setInterval(async () => {
        try {
          const res = await fetch(`${API_BASE}/${runId}/status`);
          if (res.status === 404) {
            alert("Research session lost (server restarted). Starting over.");
            handleReset();
            clearInterval(timer);
            return;
          }
          const data = await res.json();
          if (data.status === 'awaiting_approval') {
            setPlan(data.plan);
            setStatus("awaiting_approval");
            clearInterval(timer);
          }
        } catch (err) {
          console.error(err);
        }
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [runId, status]);

  const handleRunStarted = (id) => {
    setRunId(id);
    setStatus("idle");
  };

  const handleApproved = () => {
    setStatus("in_progress");
  };

  const handleCancelled = () => {
    setStatus("error");
    alert("Research cancelled");
  };

  const handleReset = () => {
    setRunId(null);
    setStatus("idle");
    setPlan([]);
    setView('landing');
  };

  return (
    <div className="app-container">
      <header>
        <img 
          src="/logo-wordmark.svg" 
          alt="Research Assistant" 
          className="logo-header"
          onClick={() => handleReset()}
          onError={(e) => {
            e.target.style.display='none';
            e.target.insertAdjacentHTML('afterend', '<h2 style="margin:0;cursor:pointer;">MARA</h2>');
          }}
        />
      </header>

      {view === 'landing' ? (
        <LandingPage onStart={() => setView('app')} />
      ) : (
        <>
          {!runId && (
            <ResearchForm onRunStarted={handleRunStarted} />
          )}

          {runId && status === "idle" && (
            <div className="panel">
              <p>Planning research approach... Please wait.</p>
            </div>
          )}

          {status === "awaiting_approval" && (
            <ApprovalPanel 
              runId={runId} 
              initialPlan={plan} 
              onApproved={handleApproved}
              onCancelled={handleCancelled}
            />
          )}

          {status === "in_progress" && (
            <ProgressPanel 
              runId={runId} 
              onComplete={() => setStatus("complete")}
              onError={() => setStatus("error")}
            />
          )}

          {status === "complete" && (
            <ReportPanel runId={runId} onReset={handleReset} />
          )}
          
          {status === "error" && (
            <div className="panel" style={{borderColor: 'var(--text-main)'}}>
              <h2>Research Failed or Cancelled</h2>
              <button className="btn" onClick={() => {
                setRunId(null);
                setStatus("idle");
              }}>Start Over</button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default App;
