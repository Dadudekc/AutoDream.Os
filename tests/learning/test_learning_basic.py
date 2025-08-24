def test_learning_agent_accumulates_knowledge(learning_agent):
    learning_agent.learn(5)
    assert learning_agent.knowledge == 5
