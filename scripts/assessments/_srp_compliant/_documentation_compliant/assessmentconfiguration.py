"""
assessmentconfiguration.py
Module: assessmentconfiguration.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:07
"""

# AssessmentConfiguration - Extracted for SRP compliance

class AssessmentConfiguration:
    """Assessment configuration settings"""
    assessment_id: str
    assessment_name: str
    target_agents: List[str]
    assessment_criteria: List[str]
    priority_threshold: IntegrationPriority
    max_assessment_time_minutes: int
    include_dependencies: bool
    generate_reports: bool
    output_format: str = "json"
    log_level: str = "INFO"



