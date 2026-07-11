import React from 'react';

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
