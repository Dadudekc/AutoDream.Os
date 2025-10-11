#!/usr/bin/env python3
"""
Data Collection Pipeline for Agent Training
==========================================

This pipeline collects and processes data from existing agent workspaces, devlogs,
and system interactions to create high-quality training datasets for autonomous
development agents.

Features:
- Multi-source data collection (agent workspaces, devlogs, vector DB, etc.)
- Data cleaning and preprocessing
- Feature extraction and engineering
- Quality assessment and filtering
- Dataset versioning and management
- Real-time data streaming capabilities

Usage:
    python scripts/data_collection_pipeline.py --collect-all --output data/training
    python scripts/data_collection_pipeline.py --stream --real-time --config configs/data_config.yaml
    python scripts/data_collection_pipeline.py --process-existing --input data/raw --output data/processed
"""

import os
import sys
import json
import argparse
import logging
import asyncio
import aiofiles
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union, AsyncGenerator
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import re
import hashlib
import numpy as np
import pandas as pd
from collections import defaultdict, Counter
import yaml

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from core.shared_logging import setup_logging
from services.vector_database.vector_database import VectorDatabase
from services.messaging.unified_messaging_service import UnifiedMessagingService

class DataSource(Enum):
    """Sources of training data."""
    AGENT_WORKSPACES = "agent_workspaces"
    DEVLOGS = "devlogs"
    VECTOR_DATABASE = "vector_database"
    MESSAGING_SYSTEM = "messaging_system"
    CODE_REPOSITORY = "code_repository"
    SYSTEM_LOGS = "system_logs"
    PERFORMANCE_METRICS = "performance_metrics"

class DataType(Enum):
    """Types of data collected."""
    CODE_SAMPLES = "code_samples"
    TASK_DESCRIPTIONS = "task_descriptions"
    AGENT_INTERACTIONS = "agent_interactions"
    QUALITY_METRICS = "quality_metrics"
    PERFORMANCE_DATA = "performance_data"
    LEARNING_PATTERNS = "learning_patterns"
    ERROR_PATTERNS = "error_patterns"

@dataclass
class DataSample:
    """A single data sample for training."""
    sample_id: str
    source: DataSource
    data_type: DataType
    content: str
    metadata: Dict[str, Any]
    quality_score: float
    created_at: datetime
    processed_at: Optional[datetime] = None
    features: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = asdict(self)
        result['created_at'] = self.created_at.isoformat()
        if self.processed_at:
            result['processed_at'] = self.processed_at.isoformat()
        return result

@dataclass
class DataCollectionConfig:
    """Configuration for data collection."""
    # Data sources to collect from
    enabled_sources: List[DataSource]
    
    # Collection parameters
    batch_size: int = 100
    max_samples_per_source: int = 10000
    quality_threshold: float = 0.5
    
    # Processing parameters
    enable_preprocessing: bool = True
    enable_feature_extraction: bool = True
    enable_quality_filtering: bool = True
    
    # Output parameters
    output_format: str = "json"  # json, parquet, csv
    compression: str = "gzip"
    chunk_size: int = 1000
    
    # Real-time parameters
    enable_streaming: bool = False
    stream_interval: float = 1.0  # seconds
    buffer_size: int = 1000

class AgentWorkspaceCollector:
    """Collects data from agent workspaces."""
    
    def __init__(self, workspace_path: str = "agent_workspaces"):
        self.workspace_path = Path(workspace_path)
        self.logger = setup_logging("agent_workspace_collector")
    
    async def collect_data(self, max_samples: int = 10000) -> List[DataSample]:
        """Collect data from agent workspaces."""
        samples = []
        
        if not self.workspace_path.exists():
            self.logger.warning(f"Agent workspace path does not exist: {self.workspace_path}")
            return samples
        
        # Collect from each agent workspace
        for agent_dir in self.workspace_path.iterdir():
            if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                agent_samples = await self._collect_agent_data(agent_dir, max_samples // 8)
                samples.extend(agent_samples)
        
        self.logger.info(f"Collected {len(samples)} samples from agent workspaces")
        return samples
    
    async def _collect_agent_data(self, agent_dir: Path, max_samples: int) -> List[DataSample]:
        """Collect data from a single agent workspace."""
        samples = []
        
        # Collect status files
        status_file = agent_dir / "status.json"
        if status_file.exists():
            sample = await self._process_status_file(status_file, agent_dir.name)
            if sample:
                samples.append(sample)
        
        # Collect inbox messages
        inbox_dir = agent_dir / "inbox"
        if inbox_dir.exists():
            inbox_samples = await self._collect_inbox_messages(inbox_dir, agent_dir.name, max_samples // 2)
            samples.extend(inbox_samples)
        
        # Collect any other relevant files
        other_samples = await self._collect_other_files(agent_dir, agent_dir.name, max_samples // 2)
        samples.extend(other_samples)
        
        return samples[:max_samples]
    
    async def _process_status_file(self, status_file: Path, agent_id: str) -> Optional[DataSample]:
        """Process agent status file."""
        try:
            async with aiofiles.open(status_file, 'r') as f:
                content = await f.read()
            
            # Parse JSON content
            status_data = json.loads(content)
            
            # Extract relevant information
            task_info = status_data.get("current_tasks", [])
            completed_tasks = status_data.get("completed_tasks", [])
            achievements = status_data.get("achievements", [])
            
            # Create combined content
            combined_content = f"Current Tasks: {task_info}\nCompleted Tasks: {completed_tasks}\nAchievements: {achievements}"
            
            # Calculate quality score
            quality_score = self._calculate_status_quality(status_data)
            
            return DataSample(
                sample_id=f"status_{agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                source=DataSource.AGENT_WORKSPACES,
                data_type=DataType.TASK_DESCRIPTIONS,
                content=combined_content,
                metadata={
                    "agent_id": agent_id,
                    "file_type": "status",
                    "file_path": str(status_file),
                    "status_data": status_data
                },
                quality_score=quality_score,
                created_at=datetime.now()
            )
        
        except Exception as e:
            self.logger.error(f"Error processing status file {status_file}: {e}")
            return None
    
    async def _collect_inbox_messages(self, inbox_dir: Path, agent_id: str, max_samples: int) -> List[DataSample]:
        """Collect inbox messages."""
        samples = []
        
        message_files = list(inbox_dir.glob("*.md"))
        for msg_file in message_files[:max_samples]:
            try:
                async with aiofiles.open(msg_file, 'r') as f:
                    content = await f.read()
                
                # Extract message metadata
                metadata = self._extract_message_metadata(content)
                
                # Calculate quality score
                quality_score = self._calculate_message_quality(content, metadata)
                
                sample = DataSample(
                    sample_id=f"inbox_{agent_id}_{msg_file.stem}",
                    source=DataSource.AGENT_WORKSPACES,
                    data_type=DataType.AGENT_INTERACTIONS,
                    content=content,
                    metadata={
                        "agent_id": agent_id,
                        "file_type": "message",
                        "file_path": str(msg_file),
                        **metadata
                    },
                    quality_score=quality_score,
                    created_at=datetime.now()
                )
                
                samples.append(sample)
            
            except Exception as e:
                self.logger.error(f"Error processing message file {msg_file}: {e}")
                continue
        
        return samples
    
    async def _collect_other_files(self, agent_dir: Path, agent_id: str, max_samples: int) -> List[DataSample]:
        """Collect other relevant files."""
        samples = []
        
        # Look for code files, logs, etc.
        for file_path in agent_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.py', '.js', '.ts', '.md', '.txt', '.log']:
                try:
                    async with aiofiles.open(file_path, 'r') as f:
                        content = await f.read()
                    
                    # Determine data type based on file extension
                    data_type = self._determine_data_type(file_path)
                    
                    # Calculate quality score
                    quality_score = self._calculate_file_quality(content, file_path)
                    
                    sample = DataSample(
                        sample_id=f"file_{agent_id}_{file_path.stem}",
                        source=DataSource.AGENT_WORKSPACES,
                        data_type=data_type,
                        content=content,
                        metadata={
                            "agent_id": agent_id,
                            "file_type": file_path.suffix,
                            "file_path": str(file_path)
                        },
                        quality_score=quality_score,
                        created_at=datetime.now()
                    )
                    
                    samples.append(sample)
                    
                    if len(samples) >= max_samples:
                        break
                
                except Exception as e:
                    self.logger.error(f"Error processing file {file_path}: {e}")
                    continue
        
        return samples
    
    def _extract_message_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from message content."""
        metadata = {}
        
        # Extract headers
        lines = content.split('\n')
        for line in lines[:10]:  # Check first 10 lines for headers
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                metadata[key] = value
        
        # Extract message type
        if 'CAPTAIN MESSAGE' in content:
            metadata['message_type'] = 'captain'
        elif 'BROADCAST' in content:
            metadata['message_type'] = 'broadcast'
        else:
            metadata['message_type'] = 'regular'
        
        # Extract priority
        if 'urgent' in content.lower():
            metadata['priority'] = 'urgent'
        elif 'high' in content.lower():
            metadata['priority'] = 'high'
        else:
            metadata['priority'] = 'normal'
        
        return metadata
    
    def _calculate_status_quality(self, status_data: Dict[str, Any]) -> float:
        """Calculate quality score for status data."""
        score = 0.0
        
        # Check required fields
        required_fields = ['agent_id', 'status', 'current_phase', 'last_updated']
        for field in required_fields:
            if field in status_data and status_data[field]:
                score += 0.25
        
        # Check data completeness
        if status_data.get('current_tasks'):
            score += 0.1
        if status_data.get('completed_tasks'):
            score += 0.1
        if status_data.get('achievements'):
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_message_quality(self, content: str, metadata: Dict[str, Any]) -> float:
        """Calculate quality score for message content."""
        score = 0.0
        
        # Length check
        if len(content) > 50:
            score += 0.2
        
        # Structure check
        if '**' in content:  # Markdown formatting
            score += 0.2
        
        # Metadata completeness
        if metadata.get('message_type'):
            score += 0.2
        if metadata.get('priority'):
            score += 0.1
        
        # Content quality indicators
        if any(keyword in content.lower() for keyword in ['task', 'implementation', 'code', 'feature']):
            score += 0.3
        
        return min(1.0, score)
    
    def _calculate_file_quality(self, content: str, file_path: Path) -> float:
        """Calculate quality score for file content."""
        score = 0.0
        
        # Length check
        if len(content) > 100:
            score += 0.2
        
        # File type specific checks
        if file_path.suffix == '.py':
            # Python specific checks
            if 'def ' in content:
                score += 0.2
            if 'class ' in content:
                score += 0.2
            if '"""' in content or "'''" in content:  # Docstrings
                score += 0.2
            if 'import ' in content:
                score += 0.1
            if 'test' in content.lower():
                score += 0.1
        elif file_path.suffix in ['.md', '.txt']:
            # Documentation specific checks
            if len(content.split('\n')) > 5:
                score += 0.3
            if '#' in content:  # Headers
                score += 0.2
            if '```' in content:  # Code blocks
                score += 0.2
        
        return min(1.0, score)
    
    def _determine_data_type(self, file_path: Path) -> DataType:
        """Determine data type based on file path."""
        if file_path.suffix in ['.py', '.js', '.ts']:
            return DataType.CODE_SAMPLES
        elif file_path.suffix in ['.md', '.txt']:
            return DataType.TASK_DESCRIPTIONS
        elif file_path.suffix == '.log':
            return DataType.PERFORMANCE_DATA
        else:
            return DataType.TASK_DESCRIPTIONS

class DevlogCollector:
    """Collects data from devlogs."""
    
    def __init__(self, devlog_path: str = "devlogs"):
        self.devlog_path = Path(devlog_path)
        self.logger = setup_logging("devlog_collector")
    
    async def collect_data(self, max_samples: int = 10000) -> List[DataSample]:
        """Collect data from devlogs."""
        samples = []
        
        if not self.devlog_path.exists():
            self.logger.warning(f"Devlog path does not exist: {self.devlog_path}")
            return samples
        
        # Collect from all devlog files
        devlog_files = list(self.devlog_path.glob("*.md"))
        for devlog_file in devlog_files[:max_samples]:
            try:
                async with aiofiles.open(devlog_file, 'r') as f:
                    content = await f.read()
                
                # Extract devlog metadata
                metadata = self._extract_devlog_metadata(content, devlog_file)
                
                # Calculate quality score
                quality_score = self._calculate_devlog_quality(content, metadata)
                
                sample = DataSample(
                    sample_id=f"devlog_{devlog_file.stem}",
                    source=DataSource.DEVLOGS,
                    data_type=DataType.TASK_DESCRIPTIONS,
                    content=content,
                    metadata={
                        "file_type": "devlog",
                        "file_path": str(devlog_file),
                        **metadata
                    },
                    quality_score=quality_score,
                    created_at=datetime.now()
                )
                
                samples.append(sample)
            
            except Exception as e:
                self.logger.error(f"Error processing devlog file {devlog_file}: {e}")
                continue
        
        self.logger.info(f"Collected {len(samples)} samples from devlogs")
        return samples
    
    def _extract_devlog_metadata(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from devlog content."""
        metadata = {}
        
        # Extract date from filename if possible
        filename = file_path.stem
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
        if date_match:
            metadata['date'] = date_match.group(1)
        
        # Extract agent information
        if 'Agent-' in content:
            agent_match = re.search(r'Agent-(\d+)', content)
            if agent_match:
                metadata['agent_id'] = f"Agent-{agent_match.group(1)}"
        
        # Extract task information
        if 'task' in content.lower():
            metadata['contains_tasks'] = True
        if 'implementation' in content.lower():
            metadata['contains_implementation'] = True
        if 'bug' in content.lower() or 'fix' in content.lower():
            metadata['contains_bug_fixes'] = True
        
        # Extract code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        metadata['code_blocks_count'] = len(code_blocks)
        
        # Extract links
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        metadata['links_count'] = len(links)
        
        return metadata
    
    def _calculate_devlog_quality(self, content: str, metadata: Dict[str, Any]) -> float:
        """Calculate quality score for devlog content."""
        score = 0.0
        
        # Length check
        if len(content) > 200:
            score += 0.2
        
        # Structure check
        if '#' in content:  # Headers
            score += 0.2
        
        # Code content
        if metadata.get('code_blocks_count', 0) > 0:
            score += 0.2
        
        # Task content
        if metadata.get('contains_tasks'):
            score += 0.2
        
        # Implementation content
        if metadata.get('contains_implementation'):
            score += 0.1
        
        # Bug fix content
        if metadata.get('contains_bug_fixes'):
            score += 0.1
        
        return min(1.0, score)

class VectorDatabaseCollector:
    """Collects data from vector database."""
    
    def __init__(self):
        self.logger = setup_logging("vector_database_collector")
        self.vector_db = None
    
    async def collect_data(self, max_samples: int = 10000) -> List[DataSample]:
        """Collect data from vector database."""
        samples = []
        
        try:
            # Initialize vector database
            self.vector_db = VectorDatabase()
            
            # Get recent embeddings and metadata
            # This would need to be implemented based on your vector DB structure
            # For now, return empty list
            pass
            
        except Exception as e:
            self.logger.error(f"Error collecting from vector database: {e}")
        
        self.logger.info(f"Collected {len(samples)} samples from vector database")
        return samples

class DataProcessor:
    """Processes collected data samples."""
    
    def __init__(self, config: DataCollectionConfig):
        self.config = config
        self.logger = setup_logging("data_processor")
    
    async def process_samples(self, samples: List[DataSample]) -> List[DataSample]:
        """Process data samples."""
        processed_samples = []
        
        for sample in samples:
            try:
                # Apply quality filtering
                if self.config.enable_quality_filtering and sample.quality_score < self.config.quality_threshold:
                    continue
                
                # Preprocess content
                if self.config.enable_preprocessing:
                    sample.content = await self._preprocess_content(sample.content, sample.data_type)
                
                # Extract features
                if self.config.enable_feature_extraction:
                    sample.features = await self._extract_features(sample)
                
                # Mark as processed
                sample.processed_at = datetime.now()
                processed_samples.append(sample)
            
            except Exception as e:
                self.logger.error(f"Error processing sample {sample.sample_id}: {e}")
                continue
        
        self.logger.info(f"Processed {len(processed_samples)} samples")
        return processed_samples
    
    async def _preprocess_content(self, content: str, data_type: DataType) -> str:
        """Preprocess content based on data type."""
        # Basic cleaning
        content = content.strip()
        
        # Remove excessive whitespace
        content = re.sub(r'\n\s*\n', '\n\n', content)
        
        # Data type specific preprocessing
        if data_type == DataType.CODE_SAMPLES:
            # Remove comments for some analysis
            content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
        
        return content
    
    async def _extract_features(self, sample: DataSample) -> Dict[str, Any]:
        """Extract features from data sample."""
        features = {}
        
        # Basic text features
        features['length'] = len(sample.content)
        features['word_count'] = len(sample.content.split())
        features['line_count'] = len(sample.content.split('\n'))
        
        # Code-specific features
        if sample.data_type == DataType.CODE_SAMPLES:
            features['function_count'] = sample.content.count('def ')
            features['class_count'] = sample.content.count('class ')
            features['import_count'] = sample.content.count('import ')
            features['comment_ratio'] = sample.content.count('#') / max(1, len(sample.content.split('\n')))
        
        # Quality features
        features['quality_score'] = sample.quality_score
        
        # Source features
        features['source'] = sample.source.value
        features['data_type'] = sample.data_type.value
        
        return features

class DataCollectionPipeline:
    """Main data collection pipeline."""
    
    def __init__(self, config: DataCollectionConfig):
        self.config = config
        self.logger = setup_logging("data_collection_pipeline")
        
        # Initialize collectors
        self.collectors = {
            DataSource.AGENT_WORKSPACES: AgentWorkspaceCollector(),
            DataSource.DEVLOGS: DevlogCollector(),
            DataSource.VECTOR_DATABASE: VectorDatabaseCollector()
        }
        
        # Initialize processor
        self.processor = DataProcessor(config)
    
    async def collect_all_data(self) -> List[DataSample]:
        """Collect data from all enabled sources."""
        all_samples = []
        
        for source in self.config.enabled_sources:
            if source in self.collectors:
                try:
                    samples = await self.collectors[source].collect_data(self.config.max_samples_per_source)
                    all_samples.extend(samples)
                    self.logger.info(f"Collected {len(samples)} samples from {source.value}")
                except Exception as e:
                    self.logger.error(f"Error collecting from {source.value}: {e}")
        
        return all_samples
    
    async def process_and_save(self, samples: List[DataSample], output_path: str):
        """Process samples and save to output path."""
        # Process samples
        processed_samples = await self.processor.process_samples(samples)
        
        # Save to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if self.config.output_format == "json":
            await self._save_json(processed_samples, output_file)
        elif self.config.output_format == "parquet":
            await self._save_parquet(processed_samples, output_file)
        elif self.config.output_format == "csv":
            await self._save_csv(processed_samples, output_file)
        
        self.logger.info(f"Saved {len(processed_samples)} processed samples to {output_file}")
    
    async def _save_json(self, samples: List[DataSample], output_file: Path):
        """Save samples as JSON."""
        data = [sample.to_dict() for sample in samples]
        
        async with aiofiles.open(output_file, 'w') as f:
            await f.write(json.dumps(data, indent=2))
    
    async def _save_parquet(self, samples: List[DataSample], output_file: Path):
        """Save samples as Parquet."""
        # Convert to DataFrame
        data = [sample.to_dict() for sample in samples]
        df = pd.DataFrame(data)
        
        # Save as Parquet
        df.to_parquet(output_file, compression=self.config.compression)
    
    async def _save_csv(self, samples: List[DataSample], output_file: Path):
        """Save samples as CSV."""
        # Convert to DataFrame
        data = [sample.to_dict() for sample in samples]
        df = pd.DataFrame(data)
        
        # Save as CSV
        df.to_csv(output_file, index=False, compression=self.config.compression)

def load_config(config_path: str) -> DataCollectionConfig:
    """Load data collection configuration."""
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    # Convert string enums to actual enums
    config_dict['enabled_sources'] = [DataSource(s) for s in config_dict['enabled_sources']]
    
    return DataCollectionConfig(**config_dict)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Data Collection Pipeline for Agent Training")
    parser.add_argument("--collect-all", action="store_true", help="Collect data from all sources")
    parser.add_argument("--stream", action="store_true", help="Enable real-time streaming")
    parser.add_argument("--real-time", action="store_true", help="Real-time data collection")
    parser.add_argument("--process-existing", action="store_true", help="Process existing data")
    parser.add_argument("--input", type=str, help="Input data path")
    parser.add_argument("--output", type=str, default="data/training", help="Output path")
    parser.add_argument("--config", type=str, help="Configuration file path")
    parser.add_argument("--max-samples", type=int, default=10000, help="Maximum samples to collect")
    parser.add_argument("--quality-threshold", type=float, default=0.5, help="Quality threshold")
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        config = load_config(args.config)
    else:
        config = DataCollectionConfig(
            enabled_sources=[DataSource.AGENT_WORKSPACES, DataSource.DEVLOGS],
            max_samples_per_source=args.max_samples,
            quality_threshold=args.quality_threshold
        )
    
    # Create pipeline
    pipeline = DataCollectionPipeline(config)
    
    async def run_collection():
        if args.collect_all:
            # Collect all data
            samples = await pipeline.collect_all_data()
            
            # Process and save
            output_file = Path(args.output) / f"collected_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            await pipeline.process_and_save(samples, str(output_file))
            
            print(f"Collected and processed {len(samples)} samples")
            print(f"Data saved to {output_file}")
        
        elif args.process_existing:
            # Process existing data
            if not args.input:
                print("Error: --input is required for processing existing data")
                return
            
            # Load existing data
            with open(args.input, 'r') as f:
                data = json.load(f)
            
            # Convert to DataSample objects
            samples = []
            for item in data:
                sample = DataSample(
                    sample_id=item['sample_id'],
                    source=DataSource(item['source']),
                    data_type=DataType(item['data_type']),
                    content=item['content'],
                    metadata=item['metadata'],
                    quality_score=item['quality_score'],
                    created_at=datetime.fromisoformat(item['created_at'])
                )
                samples.append(sample)
            
            # Process and save
            output_file = Path(args.output) / f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            await pipeline.process_and_save(samples, str(output_file))
            
            print(f"Processed {len(samples)} samples")
            print(f"Processed data saved to {output_file}")
    
    # Run async collection
    asyncio.run(run_collection())

if __name__ == "__main__":
    main()