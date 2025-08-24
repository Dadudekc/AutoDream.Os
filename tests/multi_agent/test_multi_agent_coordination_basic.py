def test_agent_network_broadcast(agent_network):
    messages = agent_network.broadcast("hello")
    assert messages == ["agent_a:hello", "agent_b:hello"]
