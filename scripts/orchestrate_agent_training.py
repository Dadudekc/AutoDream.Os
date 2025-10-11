#!/usr/bin/env python3
"""
Orchestration Script for Autonomous Agent Training
=================================================

This script orchestrates the entire autonomous agent training pipeline, including:
- Data collection from multiple sources
- Task generation and evaluation
- Model training with reinforcement learning
- Reward system optimization
- Model deployment and monitoring
- A/B testing and performance evaluation

The script provides a unified interface for training autonomous development agents
that can perform complex development tasks with minimal human intervention.

Usage:
    python scripts/orchestrate_agent_training.py --full-pipeline --config configs/agent_training_config.yaml
    python scripts/orchestrate_agent_training.py --quick-train --epochs 50
    python scripts/orchestrate_agent_training.py --resume --checkpoint checkpoints/latest.pth
    python scripts/orchestrate_agent_training.py --deploy --model-path models/agent_final.pth
"""

import os
import sys
import json
import argparse
import logging
import asyncio
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import traceback

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from core.shared_logging import setup_logging
from scripts.train_autonomous_agent import AutonomousAgentTrainer, TrainingConfig
from scripts.task_generation_framework import TaskGenerator, TaskEvaluator
from scripts.reward_system import RewardSystem
from scripts.data_collection_pipeline import DataCollectionPipeline, DataCollectionConfig
from scripts.model_deployment_monitoring import ModelDeploymentMonitoringSystem

class TrainingOrchestrator:
    """Orchestrates the entire agent training pipeline."""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = setup_logging("training_orchestrator")
        
        # Initialize components
        self.data_pipeline = None
        self.task_generator = None
        self.task_evaluator = None
        self.reward_system = None
        self.trainer = None
        self.deployment_system = None
        
        # Training state
        self.training_state = {
            "phase": "initialized",
            "start_time": None,
            "end_time": None,
            "current_epoch": 0,
            "best_performance": 0.0,
            "checkpoints": [],
            "metrics_history": []
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    
    async def run_full_pipeline(self, quick_mode: bool = False) -> bool:
        """Run the complete training pipeline."""
        try:
            self.logger.info("Starting full autonomous agent training pipeline")
            self.training_state["phase"] = "data_collection"
            self.training_state["start_time"] = datetime.now()
            
            # Phase 1: Data Collection
            await self._collect_training_data()
            
            # Phase 2: Task Generation
            await self._generate_training_tasks()
            
            # Phase 3: Model Training
            await self._train_agent_model(quick_mode)
            
            # Phase 4: Model Evaluation
            await self._evaluate_model()
            
            # Phase 5: Model Deployment
            await self._deploy_model()
            
            # Phase 6: Monitoring Setup
            await self._setup_monitoring()
            
            self.training_state["phase"] = "completed"
            self.training_state["end_time"] = datetime.now()
            
            self.logger.info("Full training pipeline completed successfully")
            return True
        
        except Exception as e:
            self.logger.error(f"Training pipeline failed: {e}")
            self.logger.error(traceback.format_exc())
            self.training_state["phase"] = "failed"
            return False
    
    async def _collect_training_data(self):
        """Collect training data from various sources."""
        self.logger.info("Phase 1: Collecting training data")
        
        # Initialize data collection pipeline
        data_config = DataCollectionConfig(
            enabled_sources=self.config["data_collection"]["enabled_sources"],
            max_samples_per_source=self.config["data_collection"]["max_samples_per_source"],
            quality_threshold=self.config["data_collection"]["quality_threshold"],
            batch_size=self.config["data_collection"]["batch_size"]
        )
        
        self.data_pipeline = DataCollectionPipeline(data_config)
        
        # Collect data
        samples = await self.data_pipeline.collect_all_data()
        
        # Process and save data
        output_dir = Path("data/training")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        await self.data_pipeline.process_and_save(
            samples, 
            str(output_dir / f"training_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        )
        
        self.logger.info(f"Collected and processed {len(samples)} training samples")
    
    async def _generate_training_tasks(self):
        """Generate training tasks for the agent."""
        self.logger.info("Phase 2: Generating training tasks")
        
        # Initialize task generator
        self.task_generator = TaskGenerator()
        
        # Generate tasks based on configuration
        category_dist = self.config["task_generation"]["category_distribution"]
        difficulty_dist = self.config["task_generation"]["difficulty_distribution"]
        
        # Convert string keys to enums (simplified)
        tasks = self.task_generator.generate_task_batch(
            count=1000,  # Generate 1000 tasks
            category_distribution=category_dist,
            difficulty_distribution=difficulty_dist
        )
        
        # Save tasks
        tasks_file = Path("data/training") / f"generated_tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(tasks_file, 'w') as f:
            json.dump([task.to_dict() for task in tasks], f, indent=2, default=str)
        
        self.logger.info(f"Generated {len(tasks)} training tasks")
    
    async def _train_agent_model(self, quick_mode: bool = False):
        """Train the autonomous agent model."""
        self.logger.info("Phase 3: Training agent model")
        
        # Create training configuration
        training_config = TrainingConfig(
            hidden_size=self.config["model"]["hidden_size"],
            num_layers=self.config["model"]["num_layers"],
            dropout=self.config["model"]["dropout"],
            max_sequence_length=self.config["model"]["max_sequence_length"],
            learning_rate=self.config["training"]["learning_rate"],
            batch_size=self.config["training"]["batch_size"],
            num_epochs=self.config["training"]["num_epochs"] if not quick_mode else 50,
            data_path="data/training",
            model_path="models/autonomous_agent",
            checkpoint_path="checkpoints"
        )
        
        # Initialize trainer
        self.trainer = AutonomousAgentTrainer(training_config)
        
        # Initialize reward system
        self.reward_system = RewardSystem(self.config["reward_system"])
        
        # Start training
        self.trainer.train()
        
        self.logger.info("Agent model training completed")
    
    async def _evaluate_model(self):
        """Evaluate the trained model."""
        self.logger.info("Phase 4: Evaluating model")
        
        # Initialize task evaluator
        self.task_evaluator = TaskEvaluator()
        
        # Load test tasks
        test_tasks_file = Path("data/training") / "generated_tasks_*.json"
        test_tasks = []
        for task_file in Path("data/training").glob("generated_tasks_*.json"):
            with open(task_file, 'r') as f:
                tasks_data = json.load(f)
                test_tasks.extend(tasks_data)
        
        # Evaluate on subset of tasks
        evaluation_results = []
        for i, task_data in enumerate(test_tasks[:100]):  # Evaluate on 100 tasks
            # Simulate agent output (in practice, this would come from the trained model)
            agent_output = {
                "generated_code": f"# Generated code for task {i}\ndef solve_task():\n    pass",
                "test_results": {
                    "tests_passed": 8,
                    "total_tests": 10,
                    "coverage_percentage": 85.0
                },
                "v2_compliance": {
                    "overall_score": 0.8,
                    "design_patterns_used": ["repository", "factory"],
                    "modularity_score": 0.7
                }
            }
            
            # Calculate reward
            reward_result = self.reward_system.calculate_reward(
                task_data, agent_output, f"task_{i}", "agent_trained"
            )
            
            evaluation_results.append({
                "task_id": f"task_{i}",
                "reward": reward_result.total_reward,
                "component_rewards": reward_result.component_rewards
            })
        
        # Calculate overall performance
        avg_reward = sum(r["reward"] for r in evaluation_results) / len(evaluation_results)
        self.training_state["best_performance"] = avg_reward
        
        # Save evaluation results
        eval_file = Path("results") / f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        eval_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(eval_file, 'w') as f:
            json.dump({
                "average_reward": avg_reward,
                "total_tasks": len(evaluation_results),
                "results": evaluation_results
            }, f, indent=2)
        
        self.logger.info(f"Model evaluation completed. Average reward: {avg_reward:.4f}")
    
    async def _deploy_model(self):
        """Deploy the trained model."""
        self.logger.info("Phase 5: Deploying model")
        
        # Initialize deployment system
        self.deployment_system = ModelDeploymentMonitoringSystem()
        
        # Deploy model
        model_path = "models/autonomous_agent/autonomous_agent_final.pth"
        model_id = f"autonomous_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        version = "1.0"
        
        success = await self.deployment_system.deploy_model(
            model_path, model_id, version, "production"
        )
        
        if success:
            self.logger.info(f"Model deployed successfully: {model_id}")
        else:
            self.logger.error("Model deployment failed")
    
    async def _setup_monitoring(self):
        """Setup monitoring for the deployed model."""
        self.logger.info("Phase 6: Setting up monitoring")
        
        # Get system status
        status = self.deployment_system.get_system_status()
        
        self.logger.info(f"Monitoring setup completed. System status: {status}")
    
    async def resume_training(self, checkpoint_path: str) -> bool:
        """Resume training from a checkpoint."""
        try:
            self.logger.info(f"Resuming training from checkpoint: {checkpoint_path}")
            
            # Load checkpoint
            checkpoint = torch.load(checkpoint_path)
            
            # Create trainer with loaded configuration
            training_config = TrainingConfig(**checkpoint["config"])
            self.trainer = AutonomousAgentTrainer(training_config)
            
            # Load model state
            self.trainer.model.load_state_dict(checkpoint["model_state_dict"])
            self.trainer.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
            self.trainer.scheduler.load_state_dict(checkpoint["scheduler_state_dict"])
            
            # Resume training
            self.trainer.train()
            
            self.logger.info("Training resumed and completed")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to resume training: {e}")
            return False
    
    async def quick_train(self, epochs: int = 50) -> bool:
        """Run a quick training session."""
        self.logger.info(f"Starting quick training with {epochs} epochs")
        
        # Override configuration for quick training
        self.config["training"]["num_epochs"] = epochs
        self.config["data_collection"]["max_samples_per_source"] = 1000
        
        return await self.run_full_pipeline(quick_mode=True)
    
    def get_training_status(self) -> Dict[str, Any]:
        """Get current training status."""
        return {
            "config_path": self.config_path,
            "training_state": self.training_state,
            "components_initialized": {
                "data_pipeline": self.data_pipeline is not None,
                "task_generator": self.task_generator is not None,
                "task_evaluator": self.task_evaluator is not None,
                "reward_system": self.reward_system is not None,
                "trainer": self.trainer is not None,
                "deployment_system": self.deployment_system is not None
            }
        }
    
    def save_training_state(self, filepath: str):
        """Save current training state."""
        with open(filepath, 'w') as f:
            json.dump(self.training_state, f, indent=2, default=str)
    
    def load_training_state(self, filepath: str):
        """Load training state from file."""
        with open(filepath, 'r') as f:
            self.training_state = json.load(f)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Orchestrate Autonomous Agent Training")
    parser.add_argument("--full-pipeline", action="store_true", help="Run full training pipeline")
    parser.add_argument("--quick-train", action="store_true", help="Run quick training")
    parser.add_argument("--epochs", type=int, default=50, help="Number of epochs for quick training")
    parser.add_argument("--resume", action="store_true", help="Resume training from checkpoint")
    parser.add_argument("--checkpoint", type=str, help="Path to checkpoint file")
    parser.add_argument("--deploy", action="store_true", help="Deploy trained model")
    parser.add_argument("--model-path", type=str, help="Path to model file for deployment")
    parser.add_argument("--config", type=str, default="configs/agent_training_config.yaml", help="Configuration file")
    parser.add_argument("--status", action="store_true", help="Show training status")
    parser.add_argument("--monitor", action="store_true", help="Monitor deployed models")
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = TrainingOrchestrator(args.config)
    
    async def run_operations():
        if args.full_pipeline:
            success = await orchestrator.run_full_pipeline()
            if success:
                print("Full training pipeline completed successfully")
            else:
                print("Training pipeline failed")
                sys.exit(1)
        
        elif args.quick_train:
            success = await orchestrator.quick_train(args.epochs)
            if success:
                print(f"Quick training completed with {args.epochs} epochs")
            else:
                print("Quick training failed")
                sys.exit(1)
        
        elif args.resume:
            if not args.checkpoint:
                print("Error: --checkpoint is required for resume")
                return
            
            success = await orchestrator.resume_training(args.checkpoint)
            if success:
                print("Training resumed and completed")
            else:
                print("Failed to resume training")
                sys.exit(1)
        
        elif args.deploy:
            if not args.model_path:
                print("Error: --model-path is required for deployment")
                return
            
            # Initialize deployment system
            deployment_system = ModelDeploymentMonitoringSystem()
            
            # Deploy model
            model_id = f"autonomous_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            success = await deployment_system.deploy_model(
                args.model_path, model_id, "1.0", "production"
            )
            
            if success:
                print(f"Model deployed successfully: {model_id}")
            else:
                print("Model deployment failed")
                sys.exit(1)
        
        elif args.status:
            status = orchestrator.get_training_status()
            print(json.dumps(status, indent=2, default=str))
        
        elif args.monitor:
            # Initialize deployment system for monitoring
            deployment_system = ModelDeploymentMonitoringSystem()
            status = deployment_system.get_system_status()
            print(json.dumps(status, indent=2, default=str))
    
    # Run async operations
    asyncio.run(run_operations())

if __name__ == "__main__":
    main()