import React, { useState } from 'react';
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
