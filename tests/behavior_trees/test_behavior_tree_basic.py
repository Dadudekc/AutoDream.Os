def test_behavior_tree_executes_child(behavior_tree):
    assert behavior_tree.children[0].execute() == "child"
