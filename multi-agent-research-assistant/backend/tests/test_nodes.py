import pytest
from app.graph.nodes import planner_node, analyzer_node, writer_node, ResearchPlan, AnalysisResult, Finding
from app.graph.state import initial_state

def test_planner_node(monkeypatch):
    state = initial_state("What are the main approaches to reducing LLM hallucination?", "run-123")
    
    class MockLLM:
        def with_structured_output(self, schema):
            return self
        def invoke(self, prompt):
            return ResearchPlan(sub_questions=[
                "What is RAG?",
                "What is fine-tuning?"
            ])
            
    monkeypatch.setattr("app.graph.nodes.get_chat_model", lambda: MockLLM())
    
    update = planner_node(state)
    assert update["status"] == "awaiting_approval"
    assert update["plan"] == ["What is RAG?", "What is fine-tuning?"]

def test_analyzer_node(monkeypatch):
    state = initial_state("test question", "run-123")
    state["plan"] = ["subq1"]
    state["research_results"] = [{"subquestion": "subq1", "source_url": "http://example.com", "title": "Test", "snippet": "Test snippet"}]
    
    class MockLLM:
        def with_structured_output(self, schema):
            return self
        def invoke(self, prompt):
            return AnalysisResult(
                findings=[Finding(claim="Test claim", supporting_source_urls=["http://example.com"])],
                needs_more_research=False,
                reasoning="Sufficient."
            )
            
    monkeypatch.setattr("app.graph.nodes.get_chat_model", lambda: MockLLM())
    
    update = analyzer_node(state)
    assert update["status"] == "analyzing"
    assert update["needs_more_research"] == False
    assert len(update["findings"]) == 1

def test_writer_node(monkeypatch):
    state = initial_state("test question", "run-123")
    state["findings"] = [{"claim": "Test claim", "supporting_sources": ["http://example.com"]}]
    
    class MockResponse:
        content = "# Report\nTest claim (http://example.com)"
        
    class MockLLM:
        def invoke(self, prompt):
            return MockResponse()
            
    monkeypatch.setattr("app.graph.nodes.get_chat_model", lambda: MockLLM())
    
    update = writer_node(state)
    assert update["status"] == "complete"
    assert "Report" in update["report"]
