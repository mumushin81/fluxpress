from pipeline.orchestrator import Pipeline
from database.client import SupabaseClient


def test_pipeline_smoke(monkeypatch):
    supabase = SupabaseClient("", "")
    # avoid filesystem writes during tests
    monkeypatch.setattr(Pipeline, "_write_local_outputs", lambda *args, **kwargs: None)
    pipeline = Pipeline(supabase)
    data = pipeline.run("https://github.com/example/repo")
    assert "draft" in data


def test_prompt_generation():
    draft = {"title": "Test", "sections": [{"title": "A", "content": "hello"}]}
    from prompts.prompt_generator import generate_prompts
    prompts = generate_prompts(draft)
    assert prompts and prompts[0]["section"] == "A"
