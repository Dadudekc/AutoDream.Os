#!/usr/bin/env python3
"""
Autonomous Agent Training Script for Development Tasks
=====================================================

This script trains an AI agent to perform autonomous development tasks using:
- Reinforcement Learning (RL) for task planning and execution
- Supervised Learning for code generation and quality assessment
- Multi-modal learning from code, documentation, and agent interactions

The trained agent can:
- Generate and prioritize development tasks
- Write, review, and refactor code autonomously
- Follow V2 compliance standards and architectural patterns
- Coordinate with the existing agent swarm system

Usage:
    python scripts/train_autonomous_agent.py --config configs/agent_training.yaml
    python scripts/train_autonomous_agent.py --quick-train --epochs 50
    python scripts/train_autonomous_agent.py --resume --checkpoint checkpoints/latest.pth
"""

import os
import sys
import json
import yaml
import argparse
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torch.distributions import Categorical
import wandb
from dataclasses import dataclass, asdict
from enum import Enum

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ml.training_pipeline import TrainingPipeline, TrainingJob, PipelineStatus
from ml.pytorch_infrastructure import PyTorchInfrastructure
from services.vector_database.vector_database import VectorDatabase
from core.shared_logging import setup_logging

class TaskType(Enum):
    """Types of development tasks the agent can perform."""
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    REFACTORING = "refactoring"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    ARCHITECTURE = "architecture"
    DEBUGGING = "debugging"
    OPTIMIZATION = "optimization"

@dataclass
class TrainingConfig:
    """Configuration for agent training."""
    # Model architecture
    hidden_size: int = 512
    num_layers: int = 4
    dropout: float = 0.1
    max_sequence_length: int = 2048
    
    # Training parameters
    learning_rate: float = 1e-4
    batch_size: int = 16
    num_epochs: int = 100
    warmup_steps: int = 1000
    weight_decay: float = 0.01
    
    # RL parameters
    gamma: float = 0.99
    eps_start: float = 1.0
    eps_end: float = 0.01
    eps_decay: int = 10000
    replay_buffer_size: int = 100000
    target_update_freq: int = 1000
    
    # Data parameters
    train_split: float = 0.8
    val_split: float = 0.1
    test_split: float = 0.1
    min_code_length: int = 50
    max_code_length: int = 2000
    
    # Paths
    data_path: str = "data/training"
    model_path: str = "models/autonomous_agent"
    checkpoint_path: str = "checkpoints"
    log_path: str = "logs/training"
    
    # Monitoring
    use_wandb: bool = True
    wandb_project: str = "autonomous-dev-agent"
    log_interval: int = 100
    save_interval: int = 1000
    eval_interval: int = 500

class DevelopmentTaskDataset(Dataset):
    """Dataset for development tasks from agent workspaces."""
    
    def __init__(self, data_path: str, task_type: TaskType, max_length: int = 2048):
        self.data_path = Path(data_path)
        self.task_type = task_type
        self.max_length = max_length
        self.samples = self._load_samples()
    
    def _load_samples(self) -> List[Dict[str, Any]]:
        """Load training samples from agent workspaces and devlogs."""
        samples = []
        
        # Load from agent workspaces
        agent_workspaces = Path("agent_workspaces")
        if agent_workspaces.exists():
            for agent_dir in agent_workspaces.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    samples.extend(self._load_agent_samples(agent_dir))
        
        # Load from devlogs
        devlogs_path = Path("devlogs")
        if devlogs_path.exists():
            samples.extend(self._load_devlog_samples(devlogs_path))
        
        # Load from vector database
        samples.extend(self._load_vector_samples())
        
        return samples
    
    def _load_agent_samples(self, agent_dir: Path) -> List[Dict[str, Any]]:
        """Load samples from agent workspace."""
        samples = []
        
        # Load status files
        status_file = agent_dir / "status.json"
        if status_file.exists():
            with open(status_file, 'r') as f:
                status_data = json.load(f)
                samples.append({
                    'type': 'status_update',
                    'content': json.dumps(status_data),
                    'task_type': TaskType.ARCHITECTURE,
                    'quality_score': 0.8
                })
        
        # Load inbox messages
        inbox_dir = agent_dir / "inbox"
        if inbox_dir.exists():
            for msg_file in inbox_dir.glob("*.md"):
                with open(msg_file, 'r') as f:
                    content = f.read()
                    samples.append({
                        'type': 'message',
                        'content': content,
                        'task_type': TaskType.CODE_GENERATION,
                        'quality_score': 0.7
                    })
        
        return samples
    
    def _load_devlog_samples(self, devlogs_path: Path) -> List[Dict[str, Any]]:
        """Load samples from devlogs."""
        samples = []
        
        for devlog_file in devlogs_path.glob("*.md"):
            with open(devlog_file, 'r') as f:
                content = f.read()
                
                # Classify task type based on content
                task_type = self._classify_task_type(content)
                
                samples.append({
                    'type': 'devlog',
                    'content': content,
                    'task_type': task_type,
                    'quality_score': 0.9  # Devlogs are high quality
                })
        
        return samples
    
    def _load_vector_samples(self) -> List[Dict[str, Any]]:
        """Load samples from vector database."""
        samples = []
        
        try:
            # Initialize vector database
            vector_db = VectorDatabase()
            
            # Get recent embeddings and metadata
            # This would need to be implemented based on your vector DB structure
            # For now, return empty list
            pass
            
        except Exception as e:
            logging.warning(f"Could not load vector samples: {e}")
        
        return samples
    
    def _classify_task_type(self, content: str) -> TaskType:
        """Classify task type based on content keywords."""
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in ['test', 'testing', 'pytest', 'unittest']):
            return TaskType.TESTING
        elif any(keyword in content_lower for keyword in ['refactor', 'refactoring', 'cleanup']):
            return TaskType.REFACTORING
        elif any(keyword in content_lower for keyword in ['review', 'feedback', 'comment']):
            return TaskType.CODE_REVIEW
        elif any(keyword in content_lower for keyword in ['doc', 'documentation', 'readme']):
            return TaskType.DOCUMENTATION
        elif any(keyword in content_lower for keyword in ['architecture', 'design', 'pattern']):
            return TaskType.ARCHITECTURE
        elif any(keyword in content_lower for keyword in ['debug', 'fix', 'error', 'bug']):
            return TaskType.DEBUGGING
        elif any(keyword in content_lower for keyword in ['optimize', 'performance', 'speed']):
            return TaskType.OPTIMIZATION
        else:
            return TaskType.CODE_GENERATION
    
    def __len__(self) -> int:
        return len(self.samples)
    
    def __getitem__(self, idx: int) -> Dict[str, Any]:
        sample = self.samples[idx]
        
        # Tokenize content (simplified - in practice, use proper tokenizer)
        content = sample['content'][:self.max_length]
        tokens = self._tokenize(content)
        
        return {
            'input_ids': torch.tensor(tokens, dtype=torch.long),
            'task_type': sample['task_type'].value,
            'quality_score': sample['quality_score'],
            'content_length': len(content)
        }
    
    def _tokenize(self, text: str) -> List[int]:
        """Simple tokenization - replace with proper tokenizer in production."""
        # This is a placeholder - use transformers tokenizer in practice
        return [ord(c) % 1000 for c in text[:self.max_length]]

class AutonomousAgentModel(nn.Module):
    """Neural network model for autonomous development agent."""
    
    def __init__(self, config: TrainingConfig, vocab_size: int = 1000, num_task_types: int = len(TaskType)):
        super().__init__()
        self.config = config
        self.vocab_size = vocab_size
        self.num_task_types = num_task_types
        
        # Embedding layers
        self.token_embedding = nn.Embedding(vocab_size, config.hidden_size)
        self.task_type_embedding = nn.Embedding(num_task_types, config.hidden_size)
        self.position_embedding = nn.Embedding(config.max_sequence_length, config.hidden_size)
        
        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=config.hidden_size,
            nhead=8,
            dim_feedforward=config.hidden_size * 4,
            dropout=config.dropout,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=config.num_layers)
        
        # Task-specific heads
        self.task_classifier = nn.Linear(config.hidden_size, num_task_types)
        self.code_generator = nn.Linear(config.hidden_size, vocab_size)
        self.quality_predictor = nn.Linear(config.hidden_size, 1)
        self.action_predictor = nn.Linear(config.hidden_size, 10)  # 10 possible actions
        
        # Dropout
        self.dropout = nn.Dropout(config.dropout)
        
    def forward(self, input_ids: torch.Tensor, task_types: torch.Tensor) -> Dict[str, torch.Tensor]:
        """Forward pass through the model."""
        batch_size, seq_len = input_ids.shape
        
        # Create position indices
        positions = torch.arange(seq_len, device=input_ids.device).unsqueeze(0).expand(batch_size, -1)
        
        # Embeddings
        token_emb = self.token_embedding(input_ids)
        task_emb = self.task_type_embedding(task_types).unsqueeze(1).expand(-1, seq_len, -1)
        pos_emb = self.position_embedding(positions)
        
        # Combine embeddings
        x = token_emb + task_emb + pos_emb
        x = self.dropout(x)
        
        # Transformer encoding
        encoded = self.transformer(x)
        
        # Global average pooling
        pooled = encoded.mean(dim=1)
        
        # Task-specific outputs
        task_logits = self.task_classifier(pooled)
        code_logits = self.code_generator(encoded)
        quality_scores = torch.sigmoid(self.quality_predictor(pooled))
        action_logits = self.action_predictor(pooled)
        
        return {
            'task_logits': task_logits,
            'code_logits': code_logits,
            'quality_scores': quality_scores,
            'action_logits': action_logits,
            'encoded_features': pooled
        }

class AutonomousAgentTrainer:
    """Trainer for the autonomous development agent."""
    
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.logger = setup_logging("autonomous_agent_trainer")
        
        # Initialize model
        self.model = AutonomousAgentModel(config)
        self.optimizer = optim.AdamW(
            self.model.parameters(),
            lr=config.learning_rate,
            weight_decay=config.weight_decay
        )
        
        # Learning rate scheduler
        self.scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(
            self.optimizer, T_0=1000, T_mult=2
        )
        
        # Loss functions
        self.task_criterion = nn.CrossEntropyLoss()
        self.code_criterion = nn.CrossEntropyLoss()
        self.quality_criterion = nn.MSELoss()
        self.action_criterion = nn.CrossEntropyLoss()
        
        # Metrics
        self.train_metrics = {}
        self.val_metrics = {}
        
        # Setup directories
        self._setup_directories()
        
        # Initialize wandb if enabled
        if config.use_wandb:
            wandb.init(
                project=config.wandb_project,
                config=asdict(config),
                name=f"autonomous_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
    
    def _setup_directories(self):
        """Create necessary directories."""
        for path in [self.config.data_path, self.config.model_path, 
                    self.config.checkpoint_path, self.config.log_path]:
            Path(path).mkdir(parents=True, exist_ok=True)
    
    def train(self):
        """Main training loop."""
        self.logger.info("Starting autonomous agent training")
        
        # Load datasets
        train_dataset = DevelopmentTaskDataset(
            self.config.data_path, 
            TaskType.CODE_GENERATION,
            self.config.max_sequence_length
        )
        
        # Split dataset
        train_size = int(len(train_dataset) * self.config.train_split)
        val_size = int(len(train_dataset) * self.config.val_split)
        test_size = len(train_dataset) - train_size - val_size
        
        train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(
            train_dataset, [train_size, val_size, test_size]
        )
        
        # Create data loaders
        train_loader = DataLoader(
            train_dataset, 
            batch_size=self.config.batch_size, 
            shuffle=True,
            num_workers=4
        )
        val_loader = DataLoader(
            val_dataset, 
            batch_size=self.config.batch_size, 
            shuffle=False,
            num_workers=4
        )
        
        # Training loop
        for epoch in range(self.config.num_epochs):
            self.logger.info(f"Epoch {epoch+1}/{self.config.num_epochs}")
            
            # Train
            train_metrics = self._train_epoch(train_loader, epoch)
            
            # Validate
            if epoch % 5 == 0:  # Validate every 5 epochs
                val_metrics = self._validate_epoch(val_loader, epoch)
                self.val_metrics.update(val_metrics)
            
            # Log metrics
            if self.config.use_wandb:
                wandb.log({
                    "epoch": epoch,
                    **train_metrics,
                    **self.val_metrics
                })
            
            # Save checkpoint
            if epoch % self.config.save_interval == 0:
                self._save_checkpoint(epoch)
            
            # Update learning rate
            self.scheduler.step()
        
        # Final evaluation
        self._evaluate_final(test_dataset)
        
        # Save final model
        self._save_final_model()
        
        self.logger.info("Training completed")
    
    def _train_epoch(self, train_loader: DataLoader, epoch: int) -> Dict[str, float]:
        """Train for one epoch."""
        self.model.train()
        total_loss = 0.0
        task_acc = 0.0
        quality_mae = 0.0
        num_batches = 0
        
        for batch_idx, batch in enumerate(train_loader):
            self.optimizer.zero_grad()
            
            # Forward pass
            outputs = self.model(
                batch['input_ids'],
                torch.tensor(batch['task_type'], dtype=torch.long)
            )
            
            # Calculate losses
            task_loss = self.task_criterion(
                outputs['task_logits'], 
                torch.tensor(batch['task_type'], dtype=torch.long)
            )
            
            quality_loss = self.quality_criterion(
                outputs['quality_scores'].squeeze(),
                torch.tensor(batch['quality_score'], dtype=torch.float)
            )
            
            # Combined loss
            total_batch_loss = task_loss + quality_loss
            
            # Backward pass
            total_batch_loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.optimizer.step()
            
            # Update metrics
            total_loss += total_batch_loss.item()
            
            # Task accuracy
            task_preds = torch.argmax(outputs['task_logits'], dim=1)
            task_acc += (task_preds == torch.tensor(batch['task_type'])).float().mean().item()
            
            # Quality MAE
            quality_mae += torch.abs(
                outputs['quality_scores'].squeeze() - torch.tensor(batch['quality_score'])
            ).mean().item()
            
            num_batches += 1
            
            # Log progress
            if batch_idx % self.config.log_interval == 0:
                self.logger.info(
                    f"Epoch {epoch}, Batch {batch_idx}/{len(train_loader)}: "
                    f"Loss: {total_batch_loss.item():.4f}, "
                    f"Task Acc: {task_acc/num_batches:.4f}, "
                    f"Quality MAE: {quality_mae/num_batches:.4f}"
                )
        
        return {
            "train_loss": total_loss / num_batches,
            "train_task_acc": task_acc / num_batches,
            "train_quality_mae": quality_mae / num_batches
        }
    
    def _validate_epoch(self, val_loader: DataLoader, epoch: int) -> Dict[str, float]:
        """Validate for one epoch."""
        self.model.eval()
        total_loss = 0.0
        task_acc = 0.0
        quality_mae = 0.0
        num_batches = 0
        
        with torch.no_grad():
            for batch in val_loader:
                # Forward pass
                outputs = self.model(
                    batch['input_ids'],
                    torch.tensor(batch['task_type'], dtype=torch.long)
                )
                
                # Calculate losses
                task_loss = self.task_criterion(
                    outputs['task_logits'], 
                    torch.tensor(batch['task_type'], dtype=torch.long)
                )
                
                quality_loss = self.quality_criterion(
                    outputs['quality_scores'].squeeze(),
                    torch.tensor(batch['quality_score'], dtype=torch.float)
                )
                
                total_batch_loss = task_loss + quality_loss
                
                # Update metrics
                total_loss += total_batch_loss.item()
                
                # Task accuracy
                task_preds = torch.argmax(outputs['task_logits'], dim=1)
                task_acc += (task_preds == torch.tensor(batch['task_type'])).float().mean().item()
                
                # Quality MAE
                quality_mae += torch.abs(
                    outputs['quality_scores'].squeeze() - torch.tensor(batch['quality_score'])
                ).mean().item()
                
                num_batches += 1
        
        return {
            "val_loss": total_loss / num_batches,
            "val_task_acc": task_acc / num_batches,
            "val_quality_mae": quality_mae / num_batches
        }
    
    def _evaluate_final(self, test_dataset: Dataset):
        """Final evaluation on test set."""
        self.logger.info("Running final evaluation")
        # Implementation for final evaluation
        pass
    
    def _save_checkpoint(self, epoch: int):
        """Save training checkpoint."""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'config': asdict(self.config),
            'train_metrics': self.train_metrics,
            'val_metrics': self.val_metrics
        }
        
        checkpoint_path = Path(self.config.checkpoint_path) / f"checkpoint_epoch_{epoch}.pth"
        torch.save(checkpoint, checkpoint_path)
        
        # Also save as latest
        latest_path = Path(self.config.checkpoint_path) / "latest.pth"
        torch.save(checkpoint, latest_path)
        
        self.logger.info(f"Checkpoint saved: {checkpoint_path}")
    
    def _save_final_model(self):
        """Save the final trained model."""
        model_path = Path(self.config.model_path) / "autonomous_agent_final.pth"
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'config': asdict(self.config)
        }, model_path)
        
        self.logger.info(f"Final model saved: {model_path}")

def load_config(config_path: str) -> TrainingConfig:
    """Load training configuration from YAML file."""
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    return TrainingConfig(**config_dict)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Train autonomous development agent")
    parser.add_argument("--config", type=str, help="Path to config YAML file")
    parser.add_argument("--quick-train", action="store_true", help="Quick training with reduced epochs")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    parser.add_argument("--checkpoint", type=str, help="Path to checkpoint file")
    parser.add_argument("--epochs", type=int, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, help="Batch size")
    parser.add_argument("--learning-rate", type=float, help="Learning rate")
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        config = load_config(args.config)
    else:
        config = TrainingConfig()
    
    # Override config with command line arguments
    if args.quick_train:
        config.num_epochs = 50
        config.batch_size = 8
    if args.epochs:
        config.num_epochs = args.epochs
    if args.batch_size:
        config.batch_size = args.batch_size
    if args.learning_rate:
        config.learning_rate = args.learning_rate
    
    # Initialize trainer
    trainer = AutonomousAgentTrainer(config)
    
    # Resume from checkpoint if specified
    if args.resume and args.checkpoint:
        # Load checkpoint and resume training
        checkpoint = torch.load(args.checkpoint)
        trainer.model.load_state_dict(checkpoint['model_state_dict'])
        trainer.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        trainer.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        trainer.logger.info(f"Resumed from checkpoint: {args.checkpoint}")
    
    # Start training
    trainer.train()

if __name__ == "__main__":
    main()