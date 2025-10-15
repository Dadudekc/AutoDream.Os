import subprocess, json

def run(cmd: list[str]) -> str:
    out = subprocess.check_output(cmd).decode()
    return out

def test_brain_note_and_search(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path/"tools").mkdir(); (tmp_path/"data/knowledge").mkdir(parents=True, exist_ok=True)
    # copy script into tmp workspace in real repo; here we assume path exists during CI
    # smoke: ensure CLI prints OK and search returns JSON
    out1 = run(["python", "tools/agent_toolbelt.py", "brain.note", "--content", "intelligent_context refactor", "--tags", "refactoring", "v2"])
    assert "OK:" in out1
    out2 = run(["python", "tools/agent_toolbelt.py", "brain.search", "--query", "refactor"])
    json.loads(out2)

def test_debate_tally(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path/"tools").mkdir(); (tmp_path/"data/knowledge").mkdir(parents=True, exist_ok=True)
    run(["python", "tools/agent_toolbelt.py", "debate.start", "--topic", "consolidation", "--participants", "A", "B"])
    run(["python", "tools/agent_toolbelt.py", "debate.vote", "--topic", "consolidation", "--voter", "A", "--choice", "yes"])
    tally = run(["python", "tools/agent_toolbelt.py", "debate.status", "--topic", "consolidation"])
    assert "tally" in tally


