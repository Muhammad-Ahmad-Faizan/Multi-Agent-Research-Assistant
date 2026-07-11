import React, { useState, useEffect } from 'react';
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
