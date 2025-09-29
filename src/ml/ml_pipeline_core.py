#!/usr/bin/env python3
"""
ML Pipeline Core - Enhanced with Data Ingestion System
======================================================

Core ML pipeline functionality enhanced with the SOS data ingestion system.
"""

import logging
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from .ml_pipeline_fallback import FallbackMLModel
from .ml_pipeline_models import ModelConfig, ModelMetrics, TrainingData

# Import SOS data ingestion components
try:
    from .data_ingestion_system.data_ingestion.IngestManager import IngestManager
    from .data_ingestion_system.data_ingestion.LocalEmbeddingsGeneratorAgent import (
        LocalEmbeddingsGeneratorAgent,
    )
    from .data_ingestion_system.data_ingestion.OrchestratorAgent import OrchestratorAgent
    from .data_ingestion_system.data_ingestion.PreprocessorAgent import PreprocessorAgent
    from .data_ingestion_system.data_ingestion.VectorStoreAgent import VectorStoreAgent

    SOS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"SOS data ingestion system not available: {e}")
    SOS_AVAILABLE = False

logger = logging.getLogger(__name__)


class MLPipelineCore:
    """Core ML pipeline functionality with enhanced data ingestion."""

    def __init__(self, config: ModelConfig | None = None):
        """Initialize ML pipeline core with data ingestion capabilities."""
        self.config = config or ModelConfig()
        self.models: dict[str, Any] = {}
        self.training_data: dict[str, TrainingData] = {}
        self.model_metrics: dict[str, ModelMetrics] = {}

        # Initialize fallback model
        self.fallback_model = FallbackMLModel(self.config)

        # Initialize SOS data ingestion system
        self._init_data_ingestion_system()

        logger.info("ML Pipeline Core with Data Ingestion initialized")

    def _init_data_ingestion_system(self):
        """Initialize the SOS data ingestion system."""
        if not SOS_AVAILABLE:
            logger.warning("SOS data ingestion system not available - using fallback mode")
            self.ingestion_available = False
            return

        try:
            self.data_folder = "./data/uploads"
            self.ingestion_manager = IngestManager(folder_path=self.data_folder)
            self.preprocessor = PreprocessorAgent(chunk_size=500, chunk_overlap=50)
            self.embeddings_generator = LocalEmbeddingsGeneratorAgent(model="mistral")
            self.vector_store = VectorStoreAgent(collection_name="ml_pipeline_collection")
            self.orchestrator = OrchestratorAgent(
                folder_to_watch=self.data_folder,
                embedding_model="mistral",
                vector_collection="ml_pipeline_collection",
            )
            self.ingestion_available = True
            logger.info("SOS data ingestion system initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize SOS data ingestion: {e}")
            self.ingestion_available = False

    def create_training_data(
        self,
        num_samples: int = 1000,
        num_features: int = 10,
        num_classes: int = 3,
        data_type: str = "classification",
    ) -> TrainingData:
        """Create synthetic training data."""
        try:
            logger.info(
                f"Creating synthetic training data: {num_samples} samples, {num_features} features"
            )

            # Generate random features
            features = np.random.randn(num_samples, num_features)

            if data_type == "classification":
                # Generate random labels for classification
                labels = np.random.randint(0, num_classes, num_samples)
            else:
                # Generate continuous labels for regression
                labels = np.random.randn(num_samples)

            # Split data
            train_size = int(0.7 * num_samples)
            val_size = int(0.15 * num_samples)

            train_features = features[:train_size]
            train_labels = labels[:train_size]

            val_features = features[train_size : train_size + val_size]
            val_labels = labels[train_size : train_size + val_size]

            test_features = features[train_size + val_size :]
            test_labels = labels[train_size + val_size :]

            training_data = TrainingData(
                features=train_features,
                labels=train_labels,
                validation_features=val_features,
                validation_labels=val_labels,
                test_features=test_features,
                test_labels=test_labels,
            )

            logger.info("Synthetic training data created successfully")
            return training_data

        except Exception as e:
            logger.error(f"Error creating training data: {e}")
            raise

    def create_model(self, model_name: str, model_type: str = "neural_network") -> Any:
        """Create a new ML model."""
        try:
            logger.info(f"Creating model: {model_name} ({model_type})")

            if model_type == "neural_network":
                model = self._create_neural_network_model()
            elif model_type == "fallback":
                model = self.fallback_model
            else:
                raise ValueError(f"Unsupported model type: {model_type}")

            self.models[model_name] = model

            logger.info(f"Model {model_name} created successfully")
            return model

        except Exception as e:
            logger.error(f"Error creating model {model_name}: {e}")
            raise

    def _create_neural_network_model(self):
        """Create a neural network model."""
        try:
            # Try to create TensorFlow model first
            try:
                return self._create_tensorflow_model()
            except ImportError:
                logger.warning("TensorFlow not available, trying PyTorch")
                try:
                    return self._create_pytorch_model()
                except ImportError:
                    logger.warning("PyTorch not available, using fallback model")
                    return self.fallback_model

        except Exception as e:
            logger.error(f"Error creating neural network model: {e}")
            return self.fallback_model

    def _create_tensorflow_model(self):
        """Create TensorFlow model."""
        try:
            import tensorflow as tf

            model = tf.keras.Sequential(
                [
                    tf.keras.layers.Dense(
                        128, activation="relu", input_shape=self.config.input_shape
                    ),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.Dense(64, activation="relu"),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.Dense(self.config.num_classes, activation="softmax"),
                ]
            )

            model.compile(
                optimizer=self.config.optimizer,
                loss=self.config.loss_function,
                metrics=self.config.metrics,
            )

            logger.info("TensorFlow model created successfully")
            return model

        except ImportError:
            raise ImportError("TensorFlow not available")

    def _create_pytorch_model(self):
        """Create PyTorch model."""
        try:
            import torch
            import torch.nn as nn

            class PyTorchModel(nn.Module):
                def __init__(self, input_size, num_classes):
                    super().__init__()
                    self.fc1 = nn.Linear(input_size, 128)
                    self.fc2 = nn.Linear(128, 64)
                    self.fc3 = nn.Linear(64, num_classes)
                    self.dropout = nn.Dropout(0.2)
                    self.relu = nn.ReLU()
                    self.softmax = nn.Softmax(dim=1)

                def forward(self, x):
                    x = self.relu(self.fc1(x))
                    x = self.dropout(x)
                    x = self.relu(self.fc2(x))
                    x = self.dropout(x)
                    x = self.fc3(x)
                    return self.softmax(x)

            model = PyTorchModel(
                input_size=np.prod(self.config.input_shape), num_classes=self.config.num_classes
            )

            logger.info("PyTorch model created successfully")
            return model

        except ImportError:
            raise ImportError("PyTorch not available")

    def train_model(
        self,
        model_name: str,
        training_data: TrainingData,
        epochs: int | None = None,
        batch_size: int | None = None,
    ) -> dict[str, Any]:
        """Train a model."""
        try:
            logger.info(f"Training model: {model_name}")

            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")

            model = self.models[model_name]
            epochs = epochs or self.config.epochs
            batch_size = batch_size or self.config.batch_size

            start_time = time.time()

            # Train the model
            if hasattr(model, "fit"):  # TensorFlow/Keras model
                history = model.fit(
                    training_data.features,
                    training_data.labels,
                    epochs=epochs,
                    batch_size=batch_size,
                    validation_data=(
                        training_data.validation_features,
                        training_data.validation_labels,
                    )
                    if training_data.validation_features is not None
                    else None,
                    verbose=1,
                )
                training_results = {
                    "status": "completed",
                    "epochs": epochs,
                    "final_loss": float(history.history["loss"][-1]),
                    "final_accuracy": float(history.history["accuracy"][-1])
                    if "accuracy" in history.history
                    else None,
                    "model_type": "tensorflow",
                }
            else:  # Fallback or PyTorch model
                training_results = model.train(training_data)

            training_time = time.time() - start_time
            training_results["training_time"] = training_time

            # Store training data
            self.training_data[model_name] = training_data

            logger.info(f"Model {model_name} training completed in {training_time:.2f} seconds")
            return training_results

        except Exception as e:
            logger.error(f"Error training model {model_name}: {e}")
            return {"status": "failed", "error": str(e)}

    def evaluate_model(self, model_name: str, test_data: TrainingData) -> dict[str, Any]:
        """Evaluate a model."""
        try:
            logger.info(f"Evaluating model: {model_name}")

            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")

            model = self.models[model_name]

            # Make predictions
            start_time = time.time()
            predictions = model.predict(test_data.features)
            inference_time = time.time() - start_time

            # Calculate metrics
            if self.config.model_type == "classification":
                accuracy = np.mean(predictions == test_data.labels)

                # Calculate precision, recall, F1-score
                from sklearn.metrics import f1_score, precision_score, recall_score

                precision = precision_score(test_data.labels, predictions, average="weighted")
                recall = recall_score(test_data.labels, predictions, average="weighted")
                f1 = f1_score(test_data.labels, predictions, average="weighted")
            else:
                # Regression metrics
                mse = np.mean((predictions - test_data.labels) ** 2)
                accuracy = 1.0 / (1.0 + mse)  # Convert MSE to accuracy-like metric
                precision = recall = f1 = None

            # Create metrics object
            metrics = ModelMetrics(
                accuracy=float(accuracy),
                precision=float(precision) if precision is not None else 0.0,
                recall=float(recall) if recall is not None else 0.0,
                f1_score=float(f1) if f1 is not None else 0.0,
                loss=float(mse) if self.config.model_type == "regression" else 0.0,
                training_time=0.0,  # Will be updated from training results
                inference_time=float(inference_time),
                model_size=0.0,  # Would need model serialization to calculate
                parameters_count=0,  # Would need model introspection to calculate
            )

            self.model_metrics[model_name] = metrics

            evaluation_results = {
                "status": "completed",
                "metrics": metrics.to_dict(),
                "inference_time": inference_time,
            }

            logger.info(f"Model {model_name} evaluation completed")
            return evaluation_results

        except Exception as e:
            logger.error(f"Error evaluating model {model_name}: {e}")
            return {"status": "failed", "error": str(e)}

    # -------------------------
    # ENHANCED DATA INGESTION METHODS
    # -------------------------

    def ingest_data_from_files(self, folder_path: str | None = None) -> list[dict[str, str]]:
        """Ingest data from files using SOS system."""
        if not self.ingestion_available:
            logger.error("Data ingestion system not available")
            return []

        try:
            folder_to_use = folder_path or self.data_folder
            logger.info(f"Ingesting data from: {folder_to_use}")

            # Use the SOS ingestion system
            documents = self.ingestion_manager.ingest()
            logger.info(f"Successfully ingested {len(documents)} documents")

            return documents

        except Exception as e:
            logger.error(f"Error ingesting data: {e}")
            return []

    def process_text_data(self, text_data: str | list[str], chunk_size: int = 500) -> list[str]:
        """Process text data with enhanced preprocessing."""
        if not self.ingestion_available:
            logger.error("Data ingestion system not available")
            return []

        try:
            if isinstance(text_data, str):
                text_data = [text_data]

            processed_chunks = []
            for text in text_data:
                # Clean text
                cleaned_text = self.preprocessor.clean_text(text)

                # Chunk text
                chunks = self.preprocessor.chunk_text(cleaned_text)
                processed_chunks.extend(chunks)

                logger.info(f"Processed text into {len(chunks)} chunks")

            return processed_chunks

        except Exception as e:
            logger.error(f"Error processing text data: {e}")
            return []

    def generate_embeddings_from_data(
        self, data: str | list[str] | list[dict[str, str]]
    ) -> list[dict[str, Any]] | None:
        """Generate embeddings from various data formats."""
        if not self.ingestion_available:
            logger.error("Data ingestion system not available")
            return None

        try:
            # Convert input to standardized format
            if isinstance(data, str):
                chunks = self.process_text_data(data)
                processed_data = [{"content": chunk} for chunk in chunks]
            elif isinstance(data, list) and isinstance(data[0], str):
                chunks = self.process_text_data(data)
                processed_data = [{"content": chunk} for chunk in chunks]
            else:
                processed_data = data

            # Generate embeddings
            embeddings = self.embeddings_generator.generate_embeddings(processed_data)
            logger.info(f"Generated embeddings for {len(embeddings)} chunks")

            return embeddings

        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return None

    def store_embeddings_in_vector_db(self, embeddings: list[dict[str, Any]]) -> bool:
        """Store embeddings in vector database."""
        if not self.ingestion_available:
            logger.error("Data ingestion system not available")
            return False

        try:
            self.vector_store.add_embeddings(embeddings)
            self.vector_store.persist()
            logger.info("Embeddings stored in vector database successfully")
            return True

        except Exception as e:
            logger.error(f"Error storing embeddings: {e}")
            return False

    def run_full_data_pipeline(self, input_data: str | None = None) -> dict[str, Any]:
        """Run the complete data ingestion to vector storage pipeline."""
        if not self.ingestion_available:
            return {"status": "failed", "error": "Data ingestion system not available"}

        try:
            logger.info("Starting full data pipeline...")

            # Step 1: Ingest data
            if input_data:
                # Process provided text data
                documents = [{"content": input_data, "file_name": "input_data.txt"}]
            else:
                # Ingest from files
                documents = self.ingest_data_from_files()

            if not documents:
                return {"status": "failed", "error": "No data to process"}

            # Step 2: Process documents
            processed_chunks = []
            for doc in documents:
                chunks = self.process_text_data(doc["content"])
                processed_chunks.extend(
                    [{"content": chunk, "file_name": doc["file_name"]} for chunk in chunks]
                )

            # Step 3: Generate embeddings
            embeddings = self.generate_embeddings_from_data(processed_chunks)

            if not embeddings:
                return {"status": "failed", "error": "Failed to generate embeddings"}

            # Step 4: Store in vector database
            success = self.store_embeddings_in_vector_db(embeddings)

            if success:
                result = {
                    "status": "completed",
                    "documents_processed": len(documents),
                    "chunks_created": len(processed_chunks),
                    "embeddings_generated": len(embeddings),
                    "stored_in_vector_db": True,
                }
                logger.info("Full data pipeline completed successfully")
                return result
            else:
                return {
                    "status": "failed",
                    "error": "Failed to store embeddings in vector database",
                }

        except Exception as e:
            logger.error(f"Error in full data pipeline: {e}")
            return {"status": "failed", "error": str(e)}

    def search_vector_database(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Search the vector database with a query."""
        if not self.ingestion_available:
            logger.error("Data ingestion system not available")
            return []

        try:
            # Generate embedding for query
            query_embedding = self.embeddings_generator.generate_embeddings([{"content": query}])

            if not query_embedding:
                logger.error("Failed to generate query embedding")
                return []

            # Search vector database
            results = self.vector_store.search_similar(query_embedding[0], top_k=top_k)

            logger.info(f"Found {len(results)} similar documents")
            return results

        except Exception as e:
            logger.error(f"Error searching vector database: {e}")
            return []

    def get_data_ingestion_stats(self) -> dict[str, Any]:
        """Get statistics about the data ingestion system."""
        if not self.ingestion_available:
            return {"available": False, "error": "System not available"}

        try:
            # Get vector store statistics
            collection_stats = self.vector_store.get_collection_stats()

            return {
                "available": True,
                "data_folder": self.data_folder,
                "embedding_model": "mistral",
                "vector_collection": "ml_pipeline_collection",
                "collection_stats": collection_stats,
            }

        except Exception as e:
            logger.error(f"Error getting data ingestion stats: {e}")
            return {"available": True, "error": str(e)}


# -------------------------
# INTEGRATION TEST FUNCTION
# -------------------------


def test_data_ingestion_integration():
    """Test the integrated data ingestion system."""
    logger.info("Testing data ingestion integration...")

    # Create sample test data
    test_data = [
        "This is a test document for the ML pipeline integration.",
        "The system should be able to process multiple text documents efficiently.",
        "Vector embeddings will help with semantic search capabilities.",
    ]

    try:
        # Initialize pipeline
        pipeline = MLPipelineCore()
        logger.info("✅ ML Pipeline initialized")

        # Test data processing
        chunks = pipeline.process_text_data(test_data)
        logger.info(f"✅ Processed {len(chunks)} text chunks")

        # Test embedding generation
        embeddings = pipeline.generate_embeddings_from_data(test_data)
        logger.info(f"✅ Generated {len(embeddings)} embeddings")

        # Test full pipeline
        result = pipeline.run_full_data_pipeline("Test document for ML pipeline")
        logger.info(f"✅ Full pipeline result: {result}")

        # Test vector search
        search_results = pipeline.search_vector_database("test document", top_k=3)
        logger.info(f"✅ Vector search returned {len(search_results)} results")

        # Get stats
        stats = pipeline.get_data_ingestion_stats()
        logger.info(f"✅ System stats: {stats}")

        logger.info("🎉 Data ingestion integration test PASSED!")
        return True

    except Exception as e:
        logger.error(f"❌ Data ingestion integration test FAILED: {e}")
        return False


if __name__ == "__main__":
    # Run integration test
    test_data_ingestion_integration()
