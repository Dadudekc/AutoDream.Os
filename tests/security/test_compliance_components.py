from dataclasses import asdict
import sqlite3
import ssl

from src.security.policy_validator import SecurityPolicyValidator
from src.security.audit_logger import AuditLogger
from src.security.compliance_reporter import ComplianceReporter
from src.security.encryption import EncryptionManager


def test_policy_validator_detects_invalid_policy(tmp_path):
    validator = SecurityPolicyValidator(config_file=str(tmp_path / "policy.yml"))
    bad_policy = asdict(validator.default_policy)
    bad_policy["password_min_length"] = 4
    result = validator.validate_policy(bad_policy)
    assert not result.is_valid
    assert any("Password minimum length" in err for err in result.errors)


def test_audit_logger_records_and_retrieves_event(tmp_path):
    db_file = tmp_path / "audit.db"
    logger = AuditLogger(db_file=str(db_file))
    logger.log_audit_event(
        user_id="user1",
        action="login",
        resource="system",
        details={"info": "test"},
        ip_address="127.0.0.1",
    )
    trail = logger.get_audit_trail(user_id="user1")
    assert trail and trail[0]["user_id"] == "user1"


def test_compliance_reporter_generates_report(tmp_path):
    db_file = tmp_path / "comp.db"
    reporter = ComplianceReporter(db_file=str(db_file))
    report = reporter.generate_compliance_report(["ISO27001"])
    assert report["standards"] == ["ISO27001"]
    assert 0 <= report["compliance_score"] <= 100
    assert report["crypto_coverage"] == 100.0

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT crypto_coverage FROM compliance_reports")
    value = cursor.fetchone()[0]
    conn.close()
    assert value == 100.0


def test_encryption_manager_round_trip(tmp_path):
    key = EncryptionManager.generate_key()
    manager = EncryptionManager(key)
    data = b"secret"
    token = manager.encrypt(data)
    assert manager.decrypt(token) == data

    plain = tmp_path / "plain.txt"
    plain.write_text("hello")
    enc = tmp_path / "enc.bin"
    dec = tmp_path / "dec.txt"
    manager.encrypt_file(str(plain), str(enc))
    manager.decrypt_file(str(enc), str(dec))
    assert dec.read_text() == "hello"

    context = EncryptionManager.create_secure_context()
    assert context.minimum_version >= ssl.TLSVersion.TLSv1_2
