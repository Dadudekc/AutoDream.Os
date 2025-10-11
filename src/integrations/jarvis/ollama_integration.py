from ..core.unified_entry_point_system import main

"""
Ollama Integration for Local Agents
Provides local LLM capabilities for our custom agents
"""


logger = logging.getLogger(__name__)


@dataclass
class OllamaResponse:
    """Response from Ollama API"""

    model: str
    response: str
    done: bool
    context: Optional[List[int]] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None


class OllamaClient:
    """Client for interacting with Ollama API"""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.session = requests.Session()
        self.logger = logging.getLogger("OllamaClient")

    def is_available(self) -> bool:
        """Check if Ollama is running and available"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except Exception as e:
            self.get_logger(__name__).warning(f"Ollama not available: {e}")
            return False

    def get_models(self) -> List[Dict[str, Any]]:
        """Get list of available models"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                return response.json().get("models", [])
            return []
        except Exception as e:
            self.get_logger(__name__).error(f"Error getting models: {e}")
            return []

    def generate(self, model: str, prompt: str, **kwargs) -> OllamaResponse:
        """Generate text using Ollama"""
        try:
            payload = {"model": model, "prompt": prompt, "stream": False, **kwargs}

            response = self.session.post(f"{self.base_url}/api/generate", json=payload, timeout=60)

            if response.status_code == 200:
                data = response.json()
                return OllamaResponse(**data)
            else:
                raise Exception(f"Ollama API error: {response.status_code}")

        except Exception as e:
            self.get_logger(__name__).error(f"Error generating text: {e}")
            raise

    async def generate_async(self, model: str, prompt: str, **kwargs) -> OllamaResponse:
        """Generate text asynchronously"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.generate(model, prompt, **kwargs))


class OllamaAgent:
    """Agent powered by Ollama LLM"""

    def __init__(self, model: str = "llama3.2", client: Optional[OllamaClient] = None):
        self.model = model
        self.client = client or OllamaClient()
        self.logger = logging.getLogger(f"OllamaAgent_{model}")

    def is_ready(self) -> bool:
        """Check if agent is ready to use"""
        return self.client.is_available()

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        models = self.client.get_models()
        for model_info in models:
            if model_info.get("name") == self.model:
                return model_info
        return {}

    def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate a response using Ollama"""
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt

            response = self.client.generate(
                model=self.model, prompt=full_prompt, temperature=0.7, max_tokens=1000
            )

            return response.response

        except Exception as e:
            self.get_logger(__name__).error(f"Error generating response: {e}")
            return f"Error: {str(e)}"

    async def generate_response_async(self, prompt: str, context: str = "") -> str:
        """Generate response asynchronously"""
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt

            response = await self.client.generate_async(
                model=self.model, prompt=full_prompt, temperature=0.7, max_tokens=1000
            )

            return response.response

        except Exception as e:
            self.get_logger(__name__).error(f"Error generating response: {e}")
            return f"Error: {str(e)}"


class OllamaCodeAgent(OllamaAgent):
    """Specialized agent for code-related tasks"""

    def __init__(self, model: str = "codellama", client: Optional[OllamaClient] = None):
        super().__init__(model, client)
        self.code_context = ""

    def set_code_context(self, code: str):
        """Set the current code context"""
        self.code_context = code

    def analyze_code(self, prompt: str) -> str:
        """Analyze code with context"""
        context = f"Code to analyze:\n{self.code_context}\n\nAnalysis request:"
        return self.generate_response(prompt, context)

    def generate_code(self, description: str) -> str:
        """Generate code based on description"""
        prompt = (
            f"Generate Python code for: {description}\n\nProvide only the code, no explanations:"
        )
        return self.generate_response(prompt)

    def review_code(self, code: str) -> str:
        """Review and suggest improvements for code"""
        prompt = f"Review this code and suggest improvements:\n\n{code}\n\nReview:"
        return self.generate_response(prompt)

    def debug_code(self, code: str, error: str) -> str:
        """Debug code with error information"""
        prompt = f"Debug this code with error:\n\nCode:\n{code}\n\nError:\n{error}\n\nFix:"
        return self.generate_response(prompt)


class OllamaVoiceAgent(OllamaAgent):
    """Agent for voice interaction and natural language processing"""

    def __init__(self, model: str = "llama3.2", client: Optional[OllamaClient] = None):
        super().__init__(model, client)

    def process_voice_command(self, command: str) -> str:
        """Process voice command and return response"""
        prompt = f"Process this voice command and provide a helpful response: {command}"
        return self.generate_response(prompt)

    def extract_intent(self, command: str) -> Dict[str, Any]:
        """Extract intent from voice command"""
        prompt = f"""
        Extract the intent from this voice command and return as JSON:
        Command: {command}
        
        Return format:
        {{
            "intent": "action_type",
            "parameters": {{}},
            "confidence": 0.0
        }}
        """

        response = self.generate_response(prompt)
        try:
            return json.loads(response)
        except:
            return {"intent": "unknown", "parameters": {}, "confidence": 0.0}


class OllamaManager:
    """Manager for multiple Ollama agents"""

    def __init__(self):
        self.agents: Dict[str, OllamaAgent] = {}
        self.client = OllamaClient()
        self.logger = logging.getLogger("OllamaManager")

    def register_agent(self, name: str, agent: OllamaAgent):
        """Register an agent"""
        self.agents[name] = agent
        self.get_logger(__name__).info(f"Registered agent: {name}")

    def get_agent(self, name: str) -> Optional[OllamaAgent]:
        """Get agent by name"""
        return self.agents.get(name)

    def is_available(self) -> bool:
        """Check if Ollama is available"""
        return self.client.is_available()

    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return [model.get("name") for model in self.client.get_models()]

    def create_code_agent(self, name: str, model: str = "codellama") -> OllamaCodeAgent:
        """Create and register a code agent"""
        agent = OllamaCodeAgent(model, self.client)
        self.register_agent(name, agent)
        return agent

    def create_voice_agent(self, name: str, model: str = "llama3.2") -> OllamaVoiceAgent:
        """Create and register a voice agent"""
        agent = OllamaVoiceAgent(model, self.client)
        self.register_agent(name, agent)
        return agent


# Example usage

if __name__ == "__main__":
    main()
