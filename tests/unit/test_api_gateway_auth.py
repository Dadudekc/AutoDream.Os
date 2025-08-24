import os
from datetime import datetime, timedelta

import jwt

from src.services.api_gateway import V2APIGateway, GatewayRequest, RouteMethod

def _create_token(secret: str, audience: str, expires: timedelta) -> str:
    payload = {
        "sub": "user",
        "aud": audience,
        "exp": datetime.utcnow() + expires,
    }
    return jwt.encode(payload, secret, algorithm="HS256")

def _make_request(token: str) -> GatewayRequest:
    return GatewayRequest(
        path="/", method=RouteMethod.GET, headers={"Authorization": f"Bearer {token}"}
    )

def _gateway(monkeypatch) -> V2APIGateway:
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    return V2APIGateway()

def test_valid_token(monkeypatch):
    gateway = _gateway(monkeypatch)
    token = _create_token("test-secret", gateway._jwt_audience, timedelta(minutes=5))
    assert gateway._validate_auth(_make_request(token))

def test_expired_token(monkeypatch):
    gateway = _gateway(monkeypatch)
    token = _create_token("test-secret", gateway._jwt_audience, timedelta(minutes=-5))
    assert not gateway._validate_auth(_make_request(token))

def test_tampered_token(monkeypatch):
    gateway = _gateway(monkeypatch)
    token = _create_token("test-secret", gateway._jwt_audience, timedelta(minutes=5))
    tampered = token + "a"
    assert not gateway._validate_auth(_make_request(tampered))
