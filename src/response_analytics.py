class ResponseAnalytics:
    """Analyze responses and generate follow-up tasks."""

    def __init__(self, db):
        self.db = db

    def analyze_and_generate_tasks(self, response_id, content, response_type, agent_id):
        analysis_result = self.analyze_content(content, response_type)
        self.db.insert_analysis(response_id, analysis_result)
        new_tasks = self.generate_tasks_from_analysis(analysis_result, agent_id, response_id)
        for task in new_tasks:
            self.db.insert_task(response_id, task)
            print(f"🚀 Generated new task: {task['title']} -> {task['agent']}")

    def analyze_content(self, content, response_type):
        analysis = {
            "type": response_type,
            "length": len(content),
            "contains_code": "def " in content or "class " in content,
            "contains_errors": bool(re.search(r'\b(error|exception)\b', content, re.IGNORECASE)),
            "contains_todos": bool(re.search(r'\b(todo|fixme)\b', content, re.IGNORECASE)),
            "contains_issues": bool(re.search(r'\b(issue|bug)\b', content, re.IGNORECASE)),
            "contains_recommendations": bool(re.search(r'\b(recommend|should)\b', content, re.IGNORECASE)),
            "completion_status": self.assess_completion_status(content, response_type),
        }
        return analysis

    def assess_completion_status(self, content, response_type):
        if response_type == "code_file":
            if "def " in content and "return " in content:
                return "likely_complete"
            if "class " in content and "def " in content:
                return "likely_complete"
            return "incomplete"
        if response_type == "analysis_report":
            if "conclusion" in content.lower() or "summary" in content.lower():
                return "likely_complete"
            return "incomplete"
        return "unknown"

    def generate_tasks_from_analysis(self, analysis, source_agent, response_id):
        new_tasks = []
        if analysis["contains_errors"]:
            new_tasks.append(
                {
                    "title": f"Debug Issues from {source_agent}",
                    "description": f"Investigate and fix errors identified by {source_agent}",
                    "agent": self.select_agent_for_task("debug"),
                    "priority": "high",
                    "dependencies": [f"response_{response_id}"],
                }
            )
        if analysis["contains_todos"]:
            new_tasks.append(
                {
                    "title": f"Implement TODOs from {source_agent}",
                    "description": f"Complete TODO items identified by {source_agent}",
                    "agent": self.select_agent_for_task("implementation"),
                    "priority": "medium",
                    "dependencies": [f"response_{response_id}"],
                }
            )
        if analysis["contains_recommendations"]:
            new_tasks.append(
                {
                    "title": f"Apply Recommendations from {source_agent}",
                    "description": f"Implement recommendations from {source_agent}",
                    "agent": self.select_agent_for_task("optimization"),
                    "priority": "medium",
                    "dependencies": [f"response_{response_id}"],
                }
            )
        if analysis["completion_status"] == "likely_complete":
            new_tasks.append(
                {
                    "title": f"Test Completed Work from {source_agent}",
                    "description": f"Verify and test the completed work from {source_agent}",
                    "agent": self.select_agent_for_task("testing"),
                    "priority": "normal",
                    "dependencies": [f"response_{response_id}"],
                }
            )
        return new_tasks

    def select_agent_for_task(self, task_type):
        agent_assignments = {
            "debug": "Agent-4",
            "implementation": "Agent-1",
            "optimization": "Agent-3",
            "testing": "Agent-2",
        }
        return agent_assignments.get(task_type, "Agent-1")

    def get_agent_progress_summary(self):
        return self.db.fetch_agent_progress_summary()
