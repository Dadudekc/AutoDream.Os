"""
API Integrations Module
Agent-2: AI & ML Framework Integration
TDD Integration Project - Agent_Cellphone_V2_Repository

Provides integrations with OpenAI, Anthropic, and PyTorch APIs
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime
import asyncio

# Try to import optional dependencies
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI package not available")

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logging.warning("Anthropic package not available")

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False
    logging.warning("PyTorch package not available")

logger = logging.getLogger(__name__)

class OpenAIIntegration:
    """OpenAI API integration for code generation and analysis"""
    
    def __init__(self, api_key: Optional[str] = None, organization: Optional[str] = None):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not available. Install with: pip install openai")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.organization = organization or os.getenv("OPENAI_ORGANIZATION")
        
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        # Configure OpenAI client
        openai.api_key = self.api_key
        if self.organization:
            openai.organization = self.organization
        
        self.default_model = "gpt-4"
        self.max_tokens = 4096
        self.temperature = 0.7
        
        logger.info("OpenAI integration initialized")
    
    def generate_code(self, prompt: str, model: Optional[str] = None, 
                     max_tokens: Optional[int] = None, temperature: Optional[float] = None) -> str:
        """Generate code using OpenAI API"""
        try:
            response = openai.ChatCompletion.create(
                model=model or self.default_model,
                messages=[
                    {"role": "system", "content": "You are an expert Python developer. Generate clean, well-documented code."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature
            )
            
            generated_code = response.choices[0].message.content
            logger.info(f"Generated code using {model or self.default_model}")
            return generated_code
            
        except Exception as e:
            logger.error(f"Error generating code with OpenAI: {e}")
            return ""
    
    def analyze_code(self, code: str, analysis_type: str = "quality") -> Dict[str, Any]:
        """Analyze code quality and provide feedback"""
        try:
            prompt = f"""
            Analyze the following Python code for {analysis_type}:
            
            {code}
            
            Provide a detailed analysis including:
            1. Code quality score (1-10)
            2. Potential improvements
            3. Best practices recommendations
            4. Security considerations
            5. Performance optimizations
            """
            
            response = openai.ChatCompletion.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": "You are a senior Python code reviewer and security expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.3
            )
            
            analysis = response.choices[0].message.content
            logger.info(f"Code analysis completed for {analysis_type}")
            
            return {
                "analysis_type": analysis_type,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "model_used": self.default_model
            }
            
        except Exception as e:
            logger.error(f"Error analyzing code with OpenAI: {e}")
            return {"error": str(e)}
    
    def generate_tests(self, code: str, test_framework: str = "pytest") -> str:
        """Generate test cases for given code"""
        try:
            prompt = f"""
            Generate comprehensive {test_framework} test cases for the following Python code:
            
            {code}
            
            Include:
            1. Unit tests for all functions/methods
            2. Edge case testing
            3. Error handling tests
            4. Mock/stub examples where appropriate
            5. Test data generation
            """
            
            response = openai.ChatCompletion.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": f"You are an expert in {test_framework} testing and Python development."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.4
            )
            
            tests = response.choices[0].message.content
            logger.info(f"Generated {test_framework} tests")
            
            return tests
            
        except Exception as e:
            logger.error(f"Error generating tests with OpenAI: {e}")
            return ""
    
    def refactor_code(self, code: str, refactoring_goal: str) -> str:
        """Refactor code based on specific goals"""
        try:
            prompt = f"""
            Refactor the following Python code to {refactoring_goal}:
            
            {code}
            
            Provide the refactored code with:
            1. Improved readability
            2. Better performance
            3. Cleaner architecture
            4. Proper error handling
            5. Documentation
            """
            
            response = openai.ChatCompletion.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": "You are a Python refactoring expert focused on clean code principles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.3
            )
            
            refactored_code = response.choices[0].message.content
            logger.info(f"Code refactoring completed for goal: {refactoring_goal}")
            
            return refactored_code
            
        except Exception as e:
            logger.error(f"Error refactoring code with OpenAI: {e}")
            return ""

class AnthropicIntegration:
    """Anthropic Claude API integration for intelligent assistance"""
    
    def __init__(self, api_key: Optional[str] = None):
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic package not available. Install with: pip install anthropic")
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("Anthropic API key not provided")
        
        # Initialize Anthropic client
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.default_model = "claude-3-sonnet-20240229"
        self.max_tokens = 4096
        self.temperature = 0.7
        
        logger.info("Anthropic integration initialized")
    
    def generate_text(self, prompt: str, model: Optional[str] = None,
                     max_tokens: Optional[int] = None, temperature: Optional[float] = None) -> str:
        """Generate text using Claude API"""
        try:
            message = self.client.messages.create(
                model=model or self.default_model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            generated_text = message.content[0].text
            logger.info(f"Generated text using {model or self.default_model}")
            return generated_text
            
        except Exception as e:
            logger.error(f"Error generating text with Claude: {e}")
            return ""
    
    def analyze_requirements(self, requirements_text: str) -> Dict[str, Any]:
        """Analyze project requirements and provide insights"""
        try:
            prompt = f"""
            Analyze the following project requirements and provide detailed insights:
            
            {requirements_text}
            
            Include:
            1. Requirements completeness assessment
            2. Potential technical challenges
            3. Implementation recommendations
            4. Risk assessment
            5. Resource estimation
            6. Alternative approaches
            """
            
            message = self.client.messages.create(
                model=self.default_model,
                max_tokens=self.max_tokens,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            analysis = message.content[0].text
            logger.info("Requirements analysis completed")
            
            return {
                "analysis_type": "requirements_analysis",
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "model_used": self.default_model
            }
            
        except Exception as e:
            logger.error(f"Error analyzing requirements with Claude: {e}")
            return {"error": str(e)}
    
    def generate_documentation(self, code: str, doc_type: str = "README") -> str:
        """Generate documentation for code"""
        try:
            prompt = f"""
            Generate {doc_type} documentation for the following Python code:
            
            {code}
            
            Include:
            1. Project overview
            2. Installation instructions
            3. Usage examples
            4. API documentation
            5. Configuration options
            6. Troubleshooting guide
            """
            
            message = self.client.messages.create(
                model=self.default_model,
                max_tokens=self.max_tokens,
                temperature=0.4,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            documentation = message.content[0].text
            logger.info(f"Generated {doc_type} documentation")
            
            return documentation
            
        except Exception as e:
            logger.error(f"Error generating documentation with Claude: {e}")
            return ""
    
    def code_review(self, code: str, focus_areas: List[str] = None) -> Dict[str, Any]:
        """Perform comprehensive code review"""
        try:
            focus_areas = focus_areas or ["quality", "security", "performance", "maintainability"]
            
            prompt = f"""
            Perform a comprehensive code review of the following Python code:
            
            {code}
            
            Focus on: {', '.join(focus_areas)}
            
            Provide:
            1. Overall assessment (1-10 scale)
            2. Specific issues found
            3. Improvement suggestions
            4. Security vulnerabilities
            5. Performance optimizations
            6. Best practices recommendations
            """
            
            message = self.client.messages.create(
                model=self.default_model,
                max_tokens=self.max_tokens,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            review = message.content[0].text
            logger.info("Code review completed")
            
            return {
                "review_type": "comprehensive",
                "focus_areas": focus_areas,
                "review": review,
                "timestamp": datetime.now().isoformat(),
                "model_used": self.default_model
            }
            
        except Exception as e:
            logger.error(f"Error performing code review with Claude: {e}")
            return {"error": str(e)}

class PyTorchIntegration:
    """PyTorch framework integration for deep learning"""
    
    def __init__(self):
        if not PYTORCH_AVAILABLE:
            raise ImportError("PyTorch package not available. Install with: pip install torch")
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.is_initialized = False
        
        logger.info(f"PyTorch integration initialized on device: {self.device}")
    
    def initialize(self) -> bool:
        """Initialize PyTorch framework"""
        try:
            # Check CUDA availability
            if torch.cuda.is_available():
                logger.info(f"CUDA available: {torch.cuda.get_device_name(0)}")
                logger.info(f"CUDA version: {torch.version.cuda}")
            
            # Set default tensor type
            if self.device.type == "cuda":
                torch.set_default_tensor_type(torch.cuda.FloatTensor)
            
            self.is_initialized = True
            logger.info("PyTorch framework initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing PyTorch: {e}")
            return False
    
    def create_neural_network(self, layers: List[int], activation: str = "relu") -> nn.Module:
        """Create a simple neural network"""
        try:
            if not self.is_initialized:
                self.initialize()
            
            class SimpleNN(nn.Module):
                def __init__(self, layer_sizes, activation_func):
                    super(SimpleNN, self).__init__()
                    self.layers = nn.ModuleList()
                    
                    for i in range(len(layer_sizes) - 1):
                        self.layers.append(nn.Linear(layer_sizes[i], layer_sizes[i + 1]))
                        
                        if i < len(layer_sizes) - 2:  # Don't add activation after last layer
                            if activation_func.lower() == "relu":
                                self.layers.append(nn.ReLU())
                            elif activation_func.lower() == "tanh":
                                self.layers.append(nn.Tanh())
                            elif activation_func.lower() == "sigmoid":
                                self.layers.append(nn.Sigmoid())
                
                def forward(self, x):
                    for layer in self.layers:
                        x = layer(x)
                    return x
            
            model = SimpleNN(layers, activation)
            model.to(self.device)
            
            logger.info(f"Created neural network with layers: {layers}")
            return model
            
        except Exception as e:
            logger.error(f"Error creating neural network: {e}")
            raise
    
    def train_model(self, model: nn.Module, train_loader: Any, 
                   epochs: int = 100, learning_rate: float = 0.001) -> Dict[str, Any]:
        """Train a PyTorch model"""
        try:
            if not self.is_initialized:
                self.initialize()
            
            model.train()
            criterion = nn.CrossEntropyLoss()
            optimizer = optim.Adam(model.parameters(), lr=learning_rate)
            
            training_history = {
                "epochs": [],
                "losses": [],
                "accuracies": []
            }
            
            for epoch in range(epochs):
                running_loss = 0.0
                correct = 0
                total = 0
                
                for data, targets in train_loader:
                    data, targets = data.to(self.device), targets.to(self.device)
                    
                    optimizer.zero_grad()
                    outputs = model(data)
                    loss = criterion(outputs, targets)
                    loss.backward()
                    optimizer.step()
                    
                    running_loss += loss.item()
                    _, predicted = torch.max(outputs.data, 1)
                    total += targets.size(0)
                    correct += (predicted == targets).sum().item()
                
                epoch_loss = running_loss / len(train_loader)
                epoch_accuracy = 100 * correct / total
                
                training_history["epochs"].append(epoch)
                training_history["losses"].append(epoch_loss)
                training_history["accuracies"].append(epoch_accuracy)
                
                if epoch % 10 == 0:
                    logger.info(f"Epoch {epoch}: Loss = {epoch_loss:.4f}, Accuracy = {epoch_accuracy:.2f}%")
            
            logger.info("Model training completed")
            return training_history
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise
    
    def evaluate_model(self, model: nn.Module, test_loader: Any) -> Dict[str, float]:
        """Evaluate a trained PyTorch model"""
        try:
            if not self.is_initialized:
                self.initialize()
            
            model.eval()
            correct = 0
            total = 0
            running_loss = 0.0
            criterion = nn.CrossEntropyLoss()
            
            with torch.no_grad():
                for data, targets in test_loader:
                    data, targets = data.to(self.device), targets.to(self.device)
                    outputs = model(data)
                    loss = criterion(outputs, targets)
                    
                    running_loss += loss.item()
                    _, predicted = torch.max(outputs.data, 1)
                    total += targets.size(0)
                    correct += (predicted == targets).sum().item()
            
            accuracy = 100 * correct / total
            avg_loss = running_loss / len(test_loader)
            
            results = {
                "accuracy": accuracy,
                "loss": avg_loss,
                "correct_predictions": correct,
                "total_samples": total
            }
            
            logger.info(f"Model evaluation completed: Accuracy = {accuracy:.2f}%, Loss = {avg_loss:.4f}")
            return results
            
        except Exception as e:
            logger.error(f"Error evaluating model: {e}")
            raise
    
    def save_model(self, model: nn.Module, path: str) -> bool:
        """Save a PyTorch model to disk"""
        try:
            if not self.is_initialized:
                self.initialize()
            
            # Create directory if it doesn't exist
            save_path = Path(path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            torch.save(model.state_dict(), path)
            logger.info(f"Model saved to: {path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False
    
    def load_model(self, path: str, model_class: nn.Module, *args, **kwargs) -> nn.Module:
        """Load a PyTorch model from disk"""
        try:
            if not self.is_initialized:
                self.initialize()
            
            model = model_class(*args, **kwargs)
            model.load_state_dict(torch.load(path, map_location=self.device))
            model.to(self.device)
            
            logger.info(f"Model loaded from: {path}")
            return model
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def get_model_summary(self, model: nn.Module) -> Dict[str, Any]:
        """Get a summary of model architecture and parameters"""
        try:
            total_params = sum(p.numel() for p in model.parameters())
            trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
            
            summary = {
                "total_parameters": total_params,
                "trainable_parameters": trainable_params,
                "non_trainable_parameters": total_params - trainable_params,
                "device": str(self.device),
                "model_class": model.__class__.__name__,
                "layers": []
            }
            
            # Analyze layers
            for name, layer in model.named_modules():
                if len(list(layer.children())) == 0:  # Leaf modules
                    layer_info = {
                        "name": name,
                        "type": layer.__class__.__name__,
                        "parameters": sum(p.numel() for p in layer.parameters()),
                        "shape": str(layer) if hasattr(layer, 'weight') else "N/A"
                    }
                    summary["layers"].append(layer_info)
            
            logger.info(f"Model summary generated: {total_params} total parameters")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating model summary: {e}")
            return {"error": str(e)}
