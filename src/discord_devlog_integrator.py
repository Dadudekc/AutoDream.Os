"""
Discord Devlog Integrator - V2 Compliance Module
Handles devlog posting and Discord webhook integration
V2 Compliance: Under 300-line limit achieved

@Author: Agent-3 - Infrastructure & DevOps Specialist
@Version: 2.0.0 - Modular Discord Devlog Integration
@License: MIT
"""


class DiscordDevlogIntegrator:
    """
    Handles devlog posting to Discord webhooks and integration.
    Provides centralized devlog management with Discord integration.
    V2 COMPLIANT: Under 300-line limit with focused responsibilities.
    """

    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.devlog_history: Dict[str, Dict[str, Any]] = {}

    def post_devlog(self, title: str, content: str, category: str = "general",
                   author: str = "Agent-3", priority: str = "normal") -> Dict[str, Any]:
        """
        Post a devlog entry to Discord webhook
        """
        result = {
            "success": False,
            "devlog_id": None,
            "error": None,
            "webhook_response": None
        }

        if not self.config_manager.is_devlog_enabled():
            result["error"] = "Devlog is disabled in configuration"
            return result

        webhook_url = self.config_manager.get_webhook_url()
        if not get_unified_validator().validate_required(webhook_url):
            result["error"] = "Webhook URL not configured"
            return result

        # Create devlog entry
        devlog_entry = self._create_devlog_entry(title, content, category, author, priority)

        # Post to Discord webhook
        webhook_result = self._post_to_webhook(devlog_entry, webhook_url)

        if webhook_result["success"]:
            result["success"] = True
            result["devlog_id"] = devlog_entry["id"]
            result["webhook_response"] = webhook_result["response"]
            self.devlog_history[devlog_entry["id"]] = devlog_entry
        else:
            result["error"] = webhook_result["error"]

        return result

    def _create_devlog_entry(self, title: str, content: str, category: str,
                           author: str, priority: str) -> Dict[str, Any]:
        """Create a formatted devlog entry"""
        devlog_id = f"devlog_{int(datetime.now().timestamp())}_{hash(title) % 10000}"

        return {
            "id": devlog_id,
            "title": title,
            "content": content,
            "category": category,
            "author": author,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
            "formatted_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def _post_to_webhook(self, devlog_entry: Dict[str, Any], webhook_url: str) -> Dict[str, Any]:
        """Post devlog entry to Discord webhook"""
        result = {
            "success": False,
            "response": None,
            "error": None
        }

        try:
            # Create Discord embed payload
            embed = self._create_devlog_embed(devlog_entry)
            payload = {"embeds": [embed]}

            # Post to webhook
            response = make_request(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            , "POST")

            if response.status_code in [200, 204]:
                result["success"] = True
                result["response"] = {"status_code": response.status_code}
            else:
                result["error"] = f"Webhook returned status {response.status_code}"

        except requests.exceptions.RequestException as e:
            result["error"] = f"Webhook request failed: {str(e)}"
        except Exception as e:
            result["error"] = f"Unexpected error: {str(e)}"

        return result

    def _create_devlog_embed(self, devlog_entry: Dict[str, Any]) -> Dict[str, Any]:
        """Create Discord embed for devlog entry"""
        color = self._get_priority_color(devlog_entry["priority"])

        embed = {
            "title": f"📋 {devlog_entry['title']}",
            "description": devlog_entry["content"][:2048],  # Discord description limit
            "color": color,
            "timestamp": devlog_entry["timestamp"],
            "footer": {
                "text": f"Author: {devlog_entry['author']} | Category: {devlog_entry['category']} | Priority: {devlog_entry['priority']}"
            },
            "fields": []
        }

        # Add additional fields if content is long
        if len(devlog_entry["content"]) > 2048:
            embed["fields"].append({
                "name": "Full Content",
                "value": devlog_entry["content"][2048:4096],
                "inline": False
            })

        return embed

    def _get_priority_color(self, priority: str) -> int:
        """Get color code for priority level"""
        colors = {
            "low": 0x3498db,      # Blue
            "normal": 0x2ecc71,  # Green
            "high": 0xf39c12,    # Orange
            "urgent": 0xe74c3c   # Red
        }
        return colors.get(priority.lower(), 0x3498db)

    def get_devlog_history(self, limit: int = 10) -> Dict[str, Any]:
        """Get recent devlog history"""
        recent_entries = list(self.devlog_history.values())[-limit:]

        return {
            "total_entries": len(self.devlog_history),
            "recent_entries": recent_entries,
            "categories": self._get_category_summary()
        }

    def _get_category_summary(self) -> Dict[str, int]:
        """Get summary of devlog entries by category"""
        categories = {}
        for entry in self.devlog_history.values():
            category = entry["category"]
            categories[category] = categories.get(category, 0) + 1
        return categories

    def search_devlogs(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search devlog entries"""
        results = []

        for entry in self.devlog_history.values():
            if category and entry["category"] != category:
                continue

            # Simple text search in title and content
            search_text = f"{entry['title']} {entry['content']}".lower()
            if query.lower() in search_text:
                results.append(entry)

        return results

    def get_devlog_stats(self) -> Dict[str, Any]:
        """Get devlog statistics"""
        if not self.devlog_history:
            return {"total_entries": 0, "categories": {}, "recent_activity": []}

        categories = {}
        priorities = {}
        recent_activity = []

        for entry in self.devlog_history.values():
            # Category stats
            cat = entry["category"]
            categories[cat] = categories.get(cat, 0) + 1

            # Priority stats
            pri = entry["priority"]
            priorities[pri] = priorities.get(pri, 0) + 1

            # Recent activity (last 5)
            if len(recent_activity) < 5:
                recent_activity.append(entry)

        return {
            "total_entries": len(self.devlog_history),
            "categories": categories,
            "priorities": priorities,
            "recent_activity": recent_activity[-5:]
        }

    def export_devlogs(self, file_path: str) -> bool:
        """Export devlog history to file"""
        try:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "total_entries": len(self.devlog_history),
                "entries": list(self.devlog_history.values())
            }

            with open(file_path, 'w') as f:
                write_json(export_data, f, indent=2, default=str)

            return True
        except Exception as e:
            get_logger(__name__).info(f"Failed to export devlogs: {e}")
            return False

    def import_devlogs(self, file_path: str) -> bool:
        """Import devlog history from file"""
        try:
            with open(file_path, 'r') as f:
                import_data = read_json(f)

            for entry in import_data.get("entries", []):
                self.devlog_history[entry["id"]] = entry

            return True
        except Exception as e:
            get_logger(__name__).info(f"Failed to import devlogs: {e}")
            return False

    def clear_devlog_history(self) -> None:
        """Clear all devlog history"""
        self.devlog_history.clear()

    def validate_webhook_url(self, url: str) -> bool:
        """Validate Discord webhook URL format"""
        if not get_unified_validator().validate_required(url):
            return False

        # Basic Discord webhook URL validation
        return "discord.com/api/webhooks/" in url and len(url.split("/")) >= 7

    def test_webhook_connection(self, webhook_url: str) -> Dict[str, Any]:
        """Test webhook connection with a simple message"""
        result = {
            "success": False,
            "response_time": None,
            "error": None
        }

        try:
            start_time = datetime.now()

            payload = {
                "content": "🧪 **Webhook Test** - Connection successful!",
                "embeds": []
            }

            response = make_request(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=5
            , "POST")

            end_time = datetime.now()
            result["response_time"] = (end_time - start_time).total_seconds()

            if response.status_code in [200, 204]:
                result["success"] = True
            else:
                result["error"] = f"HTTP {response.status_code}"

        except requests.exceptions.Timeout:
            result["error"] = "Connection timeout"
        except requests.exceptions.RequestException as e:
            result["error"] = f"Connection failed: {str(e)}"
        except Exception as e:
            result["error"] = f"Unexpected error: {str(e)}"

        return result

