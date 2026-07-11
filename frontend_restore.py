import os

base_dir = r"d:\Multi-Agent Research Assistant\multi-agent-research-assistant\frontend\src"
os.makedirs(os.path.join(base_dir, "components"), exist_ok=True)

files = {
    "main.jsx": '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
''',

    "config.js": '''export const API_BASE = "http://localhost:8000/research";''',

    "index.css": '''
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

:root {
  --primary: #6C63FF;
  --bg-color: #111111;
  --surface-color: #1A1A1A;
  --text-main: #F5F5F5;
  --text-muted: #A0A0A0;
  --border-color: rgba(255, 255, 255, 0.1);
}

body {
  margin: 0;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background-color: var(--bg-color);
  color: var(--text-main);
  line-height: 1.6;
}

.app-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4rem;
}

/* Fallback filter to turn black logo elements white. 
   Note: This turns the entire logo white, including the indigo accent. 
   Please replace the logo files with native white-stroke versions to preserve the indigo! */
.logo-header, .logo-footer {
  filter: brightness(0) invert(1);
}

.logo-header {
  height: 32px;
  cursor: pointer;
}

.logo-footer {
  height: 24px;
}

h1, h2, h3 {
  font-weight: 700;
  margin-bottom: 0.5rem;
}

h1 {
  font-size: 3rem;
  letter-spacing: -0.02em;
}

p {
  color: var(--text-muted);
}

.panel {
  background-color: var(--surface-color);
  border: 1px solid var(--border-color);
  padding: 2rem;
  margin-bottom: 2rem;
}

.btn {
  background-color: var(--primary);
  color: #ffffff;
  border: none;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  display: inline-block;
}

.btn:hover:not(:disabled) {
  opacity: 0.9;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: transparent;
  color: var(--text-main);
  border: 1px solid var(--border-color);
}
.btn-secondary:hover:not(:disabled) {
  background-color: rgba(255, 255, 255, 0.05);
}

.btn-danger {
  background-color: transparent;
  color: var(--text-main);
  border: 1px solid var(--border-color);
  padding: 0.25rem 0.5rem;
}
.btn-danger:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

textarea, input {
  width: 100%;
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  padding: 1rem;
  font-family: inherit;
  margin-bottom: 1rem;
  box-sizing: border-box;
}

textarea:focus, input:focus {
  outline: 1px solid var(--primary);
  border-color: var(--primary);
}

.plan-item {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 0.5rem;
}
.plan-item input {
  margin-bottom: 0;
}

.timeline {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.timeline-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}
.timeline-dot {
  width: 12px;
  height: 12px;
  border: 1px solid var(--border-color);
  background-color: var(--bg-color);
  margin-top: 6px;
  border-radius: 50%;
}
.timeline-item.active .timeline-dot {
  background-color: var(--primary);
  border-color: var(--primary);
}
.timeline-item.done .timeline-dot {
  background-color: var(--text-muted);
}
.timeline-content {
  flex: 1;
}

.markdown-body {
  line-height: 1.8;
}
.markdown-body a {
  color: var(--primary);
  text-decoration: underline;
}

/* Landing Page Specifics */
.hero {
  margin-bottom: 4rem;
}
.hero h1 {
  margin-bottom: 1rem;
  color: var(--text-main);
}
.hero p {
  font-size: 1.1rem;
  max-width: 600px;
  margin-bottom: 2rem;
}

.how-it-works {
  display: flex;
  gap: 1rem;
  margin-bottom: 4rem;
  flex-wrap: wrap;
}
.step-card {
  flex: 1;
  min-width: 150px;
  background-color: var(--surface-color);
  border: 1px solid var(--border-color);
  padding: 1.5rem;
}
.step-card-num {
  color: var(--primary);
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.step-card-title {
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.step-card-desc {
  font-size: 0.9rem;
  margin: 0;
  color: var(--text-muted);
}

.positioning {
  background-color: var(--surface-color);
  border: 1px solid var(--border-color);
  padding: 2rem;
  margin-bottom: 4rem;
}

.tech-stack {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 4rem;
}
.badge {
  border: 1px solid var(--border-color);
  padding: 0.25rem 0.75rem;
  font-size: 0.85rem;
  font-weight: 600;
  background-color: var(--surface-color);
}

footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--border-color);
  padding-top: 2rem;
  margin-top: 2rem;
}
''',

    "components/LandingPage.jsx": '''import React from 'react';

export default function LandingPage({ onStart }) {
  return (
    <>
      <div className="hero">
        <h1>Research, orchestrated by AI agents</h1>
        <p>
          A stateful, multi-agent ensemble that breaks down complex questions, 
          gathers information, analyzes gaps, and synthesizes structured reports 
          autonomously.
        </p>
        <button className="btn" onClick={onStart}>Start research</button>
      </div>

      <div className="how-it-works">
        <div className="step-card">
          <div className="step-card-num">01</div>
          <div className="step-card-title">Plan</div>
          <p className="step-card-desc">The planner decomposes your query into distinct facets.</p>
        </div>
        <div className="step-card">
          <div className="step-card-num">02</div>
          <div className="step-card-title">Research</div>
          <p className="step-card-desc">Agents scour the web using targeted queries.</p>
        </div>
        <div className="step-card">
          <div className="step-card-num">03</div>
          <div className="step-card-title">Analyze</div>
          <p className="step-card-desc">Findings are evaluated for redundancy and gaps.</p>
        </div>
        <div className="step-card">
          <div className="step-card-num">04</div>
          <div className="step-card-title">Write</div>
          <p className="step-card-desc">A structured, cited report is synthesized.</p>
        </div>
      </div>

      <div className="positioning">
        <h2>What this is (and isn't)</h2>
        <p style={{ margin: 0, color: 'var(--text-main)' }}>
          This is a demonstration of multi-agent orchestration, human-in-the-loop control, 
          and stateful graph design. It showcases how specialized LLM agents can collaborate 
          to execute complex workflows. It is not intended as a drop-in replacement for production 
          research platforms, but rather a functional proof-of-concept of advanced agentic patterns.
        </p>
      </div>

      <div className="tech-stack">
        <div className="badge">LangGraph</div>
        <div className="badge">FastAPI</div>
        <div className="badge">Groq</div>
        <div className="badge">Tavily</div>
        <div className="badge">React</div>
      </div>

      <footer>
        <img src="/logo.svg" alt="Logo" className="logo-footer" onError={(e) => e.target.style.display='none'} />
        <a href="https://github.com" target="_blank" rel="noreferrer" style={{color: 'var(--text-main)', textDecoration: 'none', fontWeight: 'bold'}}>GitHub</a>
      </footer>
    </>
  );
}
''',

    "App.jsx": '''import React, { useState, useEffect } from 'react';
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
''',

    "components/ApprovalPanel.jsx": '''import React, { useState, useEffect } from 'react';
import { API_BASE } from '../config';

export default function ApprovalPanel({ runId, initialPlan, onApproved, onCancelled }) {
  const [plan, setPlan] = useState([]);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (initialPlan) {
      setPlan(initialPlan);
    }
  }, [initialPlan]);

  const updatePlanItem = (idx, val) => {
    const newPlan = [...plan];
    newPlan[idx] = val;
    setPlan(newPlan);
  };

  const removePlanItem = (idx) => {
    const newPlan = [...plan];
    newPlan.splice(idx, 1);
    setPlan(newPlan);
  };

  const addPlanItem = () => {
    setPlan([...plan, ""]);
  };

  const handleDecision = async (approved) => {
    setSubmitting(true);
    try {
      await fetch(`${API_BASE}/${runId}/approve-plan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          approved,
          edited_plan: approved ? plan : null
        })
      });
      if (approved) onApproved();
      else onCancelled();
    } catch (err) {
      console.error(err);
      alert("Failed to submit decision");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="panel" style={{borderColor: 'var(--primary)'}}>
      <h2>Review Research Plan</h2>
      <p>The agent proposes the following distinct facets to research. Edit them if needed.</p>
      
      <div style={{marginBottom: '1rem'}}>
        {plan.map((q, idx) => (
          <div key={idx} className="plan-item">
            <span>{idx + 1}.</span>
            <input 
              type="text" 
              value={q} 
              onChange={e => updatePlanItem(idx, e.target.value)}
            />
            <button className="btn-danger" onClick={() => removePlanItem(idx)}>X</button>
          </div>
        ))}
      </div>
      
      <button className="btn-secondary" style={{marginBottom: '1.5rem', padding: '0.5rem 1rem'}} onClick={addPlanItem}>
        + Add facet
      </button>

      <div style={{display: 'flex', gap: '1rem'}}>
        <button className="btn" onClick={() => handleDecision(true)} disabled={submitting}>
          Approve & Start
        </button>
        <button className="btn btn-secondary" onClick={() => handleDecision(false)} disabled={submitting}>
          Cancel
        </button>
      </div>
    </div>
  );
}
''',

    "components/ResearchForm.jsx": '''import React, { useState } from 'react';
import { API_BASE } from '../config';

export default function ResearchForm({ onRunStarted }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    
    setLoading(true);
    try {
      const res = await fetch(API_BASE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      const data = await res.json();
      onRunStarted(data.run_id);
    } catch (err) {
      console.error(err);
      alert("Failed to start research");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>What would you like to research?</h2>
      <form onSubmit={handleSubmit}>
        <textarea 
          rows="4" 
          placeholder="e.g. How do vector databases like Qdrant, Pinecone, and Weaviate differ in indexing strategy, scalability, and cost — and which is best for a small RAG project vs. an enterprise one?"
          value={question}
          onChange={e => setQuestion(e.target.value)}
          disabled={loading}
        />
        <button className="btn" type="submit" disabled={loading || !question.trim()}>
          {loading ? "Planning..." : "Start Research"}
        </button>
      </form>
    </div>
  );
}
''',

    "components/ProgressPanel.jsx": '''import React, { useEffect, useState } from 'react';
import { API_BASE } from '../config';

export default function ProgressPanel({ runId, onComplete, onError }) {
  const [events, setEvents] = useState([]);
  const [currentStage, setCurrentStage] = useState('researching');

  useEffect(() => {
    const sse = new EventSource(`${API_BASE}/${runId}/stream`);
    
    sse.onmessage = (e) => {
      const data = JSON.parse(e.data);
      setEvents(prev => [...prev, data.message]);
      
      if (data.node === 'analyzing') setCurrentStage('analyzing');
      if (data.node === 'writer' || data.message === 'Report complete!') setCurrentStage('writing');
      if (data.node === 'complete') {
        setCurrentStage('complete');
        sse.close();
        onComplete();
      }
      if (data.node === 'error' || data.node === 'cancelled') {
        setCurrentStage('error');
        sse.close();
        onError();
      }
    };
    
    sse.onerror = (e) => {
      console.error("SSE error", e);
      sse.close();
      // fallback polling
      const timer = setInterval(async () => {
        try {
          const res = await fetch(`${API_BASE}/${runId}/status`);
          if (res.status === 404) {
            clearInterval(timer);
            onError();
            return;
          }
          const data = await res.json();
          if (data.status === 'complete') {
            clearInterval(timer);
            onComplete();
          } else if (data.status === 'error' || data.status === 'cancelled') {
            clearInterval(timer);
            onError();
          }
        } catch (err) {}
      }, 2000);
    };

    return () => sse.close();
  }, [runId, onComplete, onError]);

  const stages = ['researching', 'analyzing', 'writing', 'complete'];
  const stageIdx = stages.indexOf(currentStage) === -1 ? 0 : stages.indexOf(currentStage);

  return (
    <div className="panel">
      <h2>Live Progress</h2>
      <div className="timeline" style={{marginBottom: '2rem', marginTop: '1.5rem'}}>
        <div className={`timeline-item ${stageIdx >= 0 ? 'active' : ''} ${stageIdx > 0 ? 'done' : ''}`}>
          <div className="timeline-dot"></div>
          <div className="timeline-content">Researching (Agents fetching data)</div>
        </div>
        <div className={`timeline-item ${stageIdx >= 1 ? 'active' : ''} ${stageIdx > 1 ? 'done' : ''}`}>
          <div className="timeline-dot"></div>
          <div className="timeline-content">Analyzing (Evaluating findings & gaps)</div>
        </div>
        <div className={`timeline-item ${stageIdx >= 2 ? 'active' : ''} ${stageIdx > 2 ? 'done' : ''}`}>
          <div className="timeline-dot"></div>
          <div className="timeline-content">Writing (Synthesizing report)</div>
        </div>
      </div>
      
      <div style={{border: '1px solid var(--border-color)', padding: '1rem', maxHeight: '200px', overflowY: 'auto', fontSize: '0.9rem', color: 'var(--text-muted)'}}>
        {events.map((ev, i) => (
          <div key={i} style={{marginBottom: '0.25rem'}}>&gt; {ev}</div>
        ))}
      </div>
    </div>
  );
}
''',

    "components/ReportPanel.jsx": '''import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { API_BASE } from '../config';

export default function ReportPanel({ runId, onReset }) {
  const [report, setReport] = useState("");

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const res = await fetch(`${API_BASE}/${runId}/status`);
        const data = await res.json();
        setReport(data.report || "No report generated.");
      } catch (e) {
        setReport("Failed to load report.");
      }
    };
    fetchReport();
  }, [runId]);

  return (
    <div className="panel" style={{border: 'none', padding: '0'}}>
      <div className="markdown-body">
        <ReactMarkdown>{report}</ReactMarkdown>
      </div>
      <button className="btn" style={{marginTop: '2rem'}} onClick={onReset}>
        Start New Research
      </button>
    </div>
  );
}
'''
}

for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Frontend restored and redesign applied")
