import React, { useEffect, useState } from 'react';
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
      <div className="markdown-body">
        <ReactMarkdown>{report}</ReactMarkdown>
      </div>
      <button className="btn" style={{marginTop: '2rem'}} onClick={onReset}>
        Start New Research
      </button>
    </div>
  );
}
