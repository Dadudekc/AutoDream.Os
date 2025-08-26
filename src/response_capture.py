import hashlib
import re
from pathlib import Path


class ResponseCapture:
    """Capture agent responses and trigger analytics."""

    def __init__(self, db, analytics):
        self.db = db
        self.analytics = analytics
        self.response_patterns = {
            "code_file": r"\.py$|\.js$|\.ts$|\.java$|\.cpp$|\.h$",
            "documentation": r"\.md$|\.txt$|\.rst$|\.docx?$",
            "data_file": r"\.json$|\.xml$|\.csv$|\.yaml$|\.yml$",
            "image_file": r"\.png$|\.jpg$|\.jpeg$|\.gif$|\.svg$",
            "log_file": r"\.log$|\.out$|\.err$",
        }

    def classify_response(self, file_path: Path, content: str) -> str:
        filename = file_path.name.lower()
        for response_type, pattern in self.response_patterns.items():
            if re.search(pattern, filename):
                return response_type
        if "def " in content or "class " in content:
            return "code_file"
        elif re.search(r'\b(error|exception)\b', content, re.IGNORECASE):
            return "error_report"
        elif re.search(r'\b(analysis|report)\b', content, re.IGNORECASE):
            return "analysis_report"
        elif re.search(r'\b(task|todo)\b', content, re.IGNORECASE):
            return "task_update"
        return "unknown"

    def capture_response(self, agent_id: str, response_file_path: str) -> bool:
        try:
            file_path = Path(response_file_path)
            if not file_path.exists():
                return False
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            response_type = self.classify_response(file_path, content)
            response_id = self.db.insert_response(
                agent_id,
                str(file_path),
                content,
                content_hash,
                response_type,
                file_path.stat().st_size,
            )
            if response_id:
                print(
                    f"✅ Captured response from {agent_id}: {file_path.name} ({response_type})"
                )
                self.analytics.analyze_and_generate_tasks(
                    response_id, content, response_type, agent_id
                )
                return True
            return False
        except Exception as e:
            print(f"❌ Error capturing response: {e}")
            return False
