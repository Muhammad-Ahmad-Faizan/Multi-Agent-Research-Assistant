import React, { useEffect, useState } from 'react';
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
