import pytest
from app.graph.build_graph import build_graph
from app.graph.nodes import ResearchPlan, AnalysisResult, Finding

@pytest.mark.asyncio
async def test_full_graph(monkeypatch):
    def mock_get_chat_model():
        class UnifiedMockLLM:
            def with_structured_output(self, schema):
                self.schema = schema
                return self
            def invoke(self, prompt):
                if hasattr(self, "schema") and self.schema == ResearchPlan:
                    return ResearchPlan(sub_questions=["What is RAG?"])
                elif hasattr(self, "schema") and self.schema == AnalysisResult:
                    return AnalysisResult(
                        findings=[Finding(claim="RAG uses retrieval", supporting_source_urls=["http://test.com"])],
                        needs_more_research=False,
                        reasoning="done"
                    )
                class MockResp:
                    content = "# Final Report"
                return MockResp()
        return UnifiedMockLLM()
        
    monkeypatch.setattr("app.graph.nodes.get_chat_model", mock_get_chat_model)
    
    async def mock_search_web(q):
        return [{"source_url": "http://test.com", "title": "Test", "snippet": "Test snippet"}]
    
    monkeypatch.setattr("app.graph.nodes.search_web", mock_search_web)
    
    graph = build_graph(interrupt=False)
    
    config = {"configurable": {"thread_id": "test_thread"}}
    
    final_state = None
    async for s in graph.astream({"original_question": "Test?", "run_id": "run-123"}, config=config):
        for key, value in s.items():
            final_state = value
            
    assert final_state["status"] == "complete"
    assert final_state["report"] == "# Final Report"
