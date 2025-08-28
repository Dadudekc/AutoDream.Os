from src.services.validation_runner import ValidationRunner


def test_configuration_driven_runner_enables_and_disables_rules():
    runner = ValidationRunner()
    config = {
        "rules": {
            "enable": ["quality_standard"],
            "disable": ["deadline_check", "resource_limit", "dependency_check"],
        },
        "contract": {
            "contract_id": "c1",
            "quality_score": 50,
            "minimum_standard": 80,
        },
    }
    outcome = runner.run(config)
    results = outcome["results"]
    assert len(results) == 1
    result = results[0]
    assert result.rule_id == "quality_standard"
    assert not result.passed
    assert outcome["violations"][0].violation_type.value == "quality_below_standard"
