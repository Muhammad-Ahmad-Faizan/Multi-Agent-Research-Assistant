import os

base_dir = r"d:\Multi-Agent Research Assistant\multi-agent-research-assistant\frontend\src"
os.makedirs(os.path.join(base_dir, "components"), exist_ok=True)

files = {
    "config.js": '''export const API_BASE = "http://localhost:8000/research";\n''',
    
    "index.css": '''
:root {
  --primary-color: #6366f1;
  --primary-hover: #4f46e5;
  --bg-color: #0f172a;
  --surface-color: #1e293b;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --border-color: #334155;
  --success: #10b981;
  --error: #ef4444;
}

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  background-color: var(--bg-color);
  color: var(--text-main);
  line-height: 1.6;
}

.app-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

header {
  text-align: center;
  margin-bottom: 3rem;
}

h1 {
  font-size: 2.5rem;
  background: linear-gradient(to right, #818cf8, #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.panel {
  background-color: var(--surface-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease;
}

.panel.highlight {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

.btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
}

.btn:hover:not(:disabled) {
  background-color: var(--primary-hover);
}

.btn:active:not(:disabled) {
  transform: scale(0.98);
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: transparent;
  border: 1px solid var(--border-color);
}
.btn-secondary:hover:not(:disabled) {
  background-color: rgba(255, 255, 255, 0.05);
}

.btn-danger {
  background-color: transparent;
  color: var(--error);
  border: 1px solid var(--error);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}
.btn-danger:hover {
  background-color: rgba(239, 68, 68, 0.1);
}

textarea, input {
  width: 100%;
  background-color: #0f172a;
  border: 1px solid var(--border-color);
  color: var(--text-main);
  padding: 0.75rem;
  border-radius: 8px;
  font-family: inherit;
  margin-bottom: 1rem;
  box-sizing: border-box;
}

textarea:focus, input:focus {
  outline: none;
  border-color: var(--primary-color);
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
  gap: 1rem;
}

.timeline-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}
.timeline-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: var(--border-color);
  margin-top: 6px;
}
.timeline-item.active .timeline-dot {
  background-color: var(--primary-color);
  box-shadow: 0 0 8px var(--primary-color);
}
.timeline-item.done .timeline-dot {
  background-color: var(--success);
}
.timeline-content {
  flex: 1;
}

.markdown-body {
  line-height: 1.8;
}
.markdown-body h1, .markdown-body h2, .markdown-body h3 {
  color: var(--primary-color);
}
.markdown-body a {
  color: #818cf8;
  text-decoration: none;
}
.markdown-body a:hover {
  text-decoration: underline;
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
          placeholder="e.g. What are the main approaches to reducing LLM hallucination?"
          value={question}
          onChange={e => setQuestion(e.target.value)}
          disabled={loading}
        />
        <button className="btn" type="submit" disabled={loading || !question.trim()}>
          {loading ? "Planning research approach..." : "Start Research"}
        </button>
      </form>
    </div>
  );
}
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
    <div className="panel highlight">
      <h2>Review Research Plan</h2>
      <p style={{color: 'var(--text-muted)'}}>The agent proposes the following sub-questions. Edit them if needed.</p>
      
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
      
      <button className="btn-secondary" style={{marginBottom: '1.5rem'}} onClick={addPlanItem}>
        + Add sub-question
      </button>

      <div style={{display: 'flex', gap: '1rem'}}>
        <button className="btn" onClick={() => handleDecision(true)} disabled={submitting}>
          Approve & Start Research
        </button>
        <button className="btn btn-secondary" onClick={() => handleDecision(false)} disabled={submitting}>
          Cancel
        </button>
      </div>
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
      <div className="timeline" style={{marginBottom: '1.5rem'}}>
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
      
      <div style={{background: 'var(--bg-color)', padding: '1rem', borderRadius: '8px', maxHeight: '200px', overflowY: 'auto', fontSize: '0.9rem', color: 'var(--text-muted)'}}>
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
    <div className="panel">
      <h2>Final Research Report</h2>
      <div className="markdown-body">
        <ReactMarkdown>{report}</ReactMarkdown>
      </div>
      <button className="btn" style={{marginTop: '2rem'}} onClick={onReset}>
        Start New Research
      </button>
    </div>
  );
}
''',

    "App.jsx": '''import React, { useState, useEffect } from 'react';
import ResearchForm from './components/ResearchForm';
import ApprovalPanel from './components/ApprovalPanel';
import ProgressPanel from './components/ProgressPanel';
import ReportPanel from './components/ReportPanel';
import { API_BASE } from './config';

function App() {
  const [runId, setRunId] = useState(null);
  const [status, setStatus] = useState("idle");
  const [plan, setPlan] = useState([]);
  
  // Polling for plan when run is starting
  useEffect(() => {
    if (runId && status === "idle") {
      const timer = setInterval(async () => {
        try {
          const res = await fetch(`${API_BASE}/${runId}/status`);
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
  };

  return (
    <div className="app-container">
      <header>
        <h1>Multi-Agent Research Assistant</h1>
        <p style={{color: 'var(--text-muted)'}}>An autonomous agent ensemble that plans, searches, and synthesizes reports.</p>
      </header>

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
        <div className="panel" style={{borderColor: 'var(--error)'}}>
          <h2 style={{color: 'var(--error)'}}>Research Failed or Cancelled</h2>
          <button className="btn" onClick={handleReset}>Start Over</button>
        </div>
      )}
    </div>
  );
}

export default App;
'''
}

for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Frontend scaffolding complete")
