import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gaming_systems.osrs.ai.behavior_tree import (
    OSRSBehaviorNodeType,
    OSRSActionNode,
    OSRSConditionNode,
    OSRSSequenceNode,
    OSRSSelectorNode,
    OSRSBehaviorTree,
)


def test_node_types_enum():
    assert OSRSBehaviorNodeType.ACTION.value == "action"
    assert OSRSBehaviorNodeType.SELECTOR.value == "selector"


def test_action_and_condition_execution():
    action = OSRSActionNode("a", action_func=lambda p, s: True)
    condition = OSRSConditionNode("c", condition_func=lambda p, s: True)
    assert action.execute(None, {})
    assert condition.execute(None, {})


def test_sequence_and_selector():
    seq = OSRSSequenceNode("seq")
    seq.add_child(OSRSActionNode("a1", lambda p, s: True))
    seq.add_child(OSRSActionNode("a2", lambda p, s: False))
    assert not seq.execute(None, {})

    sel = OSRSSelectorNode("sel")
    sel.add_child(OSRSActionNode("b1", lambda p, s: False))
    sel.add_child(OSRSActionNode("b2", lambda p, s: True))
    assert sel.execute(None, {})


def test_behavior_tree_execute():
    tree = OSRSBehaviorTree("t")
    action = OSRSActionNode("a", action_func=lambda p, s: True)
    tree.set_root(action)
    assert tree.execute(None, {})
