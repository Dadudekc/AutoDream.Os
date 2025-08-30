from dataclasses import dataclass


@dataclass
class OrchestrationConfig:
    """Configuration for automation orchestration"""

    max_concurrent_automations: int = 3
    automation_timeout: int = 300  # 5 minutes
    screenshot_interval: int = 30  # Take screenshots every 30 seconds
    log_level: str = "INFO"
    enable_monitoring: bool = True
    save_artifacts: bool = True
    artifacts_dir: str = "automation_artifacts"


# Example pipeline configurations
EXAMPLE_PIPELINES = {
    "basic_website": {
        "website_generation": {
            "name": "example_site",
            "title": "Example Website",
            "description": "A basic example website",
            "pages": [
                {
                    "name": "home",
                    "title": "Home",
                    "route": "/",
                    "content": {
                        "heading": "Welcome",
                        "description": "Welcome to our site",
                    },
                }
            ],
        },
        "testing": {},
    },
    "automation_demo": {
        "web_automation": {
            "headless": True,
            "browser_type": "chrome",
            "tasks": [
                {"type": "navigation", "url": "https://example.com"},
                {"type": "screenshot", "filename": "example_site"},
            ],
        },
        "testing": {},
    },
}
