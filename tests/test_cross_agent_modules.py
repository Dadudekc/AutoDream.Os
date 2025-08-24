import datetime

from src.web.integration.authentication import AuthenticationManager
from src.web.integration.routing import MessageRouter
from src.web.integration.handshake import HandshakeNegotiator
from src.web.integration.logging_utils import get_logger
from src.web.integration.cross_agent_protocol import PROTOCOL_VERSION


def test_authentication_generate_and_revoke_token():
    auth = AuthenticationManager("secret")
    token = auth.generate_agent_token("agent1", expires_in=60)
    assert auth.validate_agent_token(token) == "agent1"
    assert auth.revoke_agent_token("agent1") is True
    assert auth.validate_agent_token(token) is None


def test_message_router_routes_and_responds():
    captured = {}

    def send_response(message, success, payload):
        captured["message"] = message
        captured["success"] = success
        captured["payload"] = payload

    router = MessageRouter(get_logger("router-test"), send_response=send_response)

    called = {}

    def handler(msg):
        called["handled"] = True
        return "ok"

    router.register_handler("command", handler)
    message = {
        "message_id": "1",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "sender_id": "agentA",
        "message_type": "command",
        "requires_response": True,
    }
    router.route(message)
    assert called.get("handled")
    assert captured["success"] is True
    assert captured["payload"]["result"] == "ok"


def test_handshake_negotiation():
    auth = AuthenticationManager("secret")
    token = auth.generate_agent_token("agentA")
    negotiator = HandshakeNegotiator(auth, PROTOCOL_VERSION, get_logger("handshake"))
    assert negotiator.negotiate("agentA", token, PROTOCOL_VERSION)
    assert not negotiator.negotiate("agentB", token, PROTOCOL_VERSION)
    assert not negotiator.negotiate("agentA", token, "0.0.1")
