#!/usr/bin/env python3
"""
Embedding Service Tests - Agent Cellphone V2
==========================================

Unit tests for embedding service functionality.

Author: Agent-7 - Web Development Specialist
License: MIT
"""



class TestEmbeddingService:
    """Test EmbeddingService functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.service = EmbeddingService(EmbeddingModel.SENTENCE_TRANSFORMERS)
    
    def test_embedding_service_initialization(self):
        """Test service initialization."""
        assert self.service.model == EmbeddingModel.SENTENCE_TRANSFORMERS
        assert self.service._sentence_transformer is None
        assert self.service._openai_client is None
    
    @patch('src.services.embedding_service.SentenceTransformer')
    def test_get_sentence_transformer(self, mock_transformer):
        """Test lazy loading of sentence transformer."""
        mock_model = Mock()
        mock_transformer.return_value = mock_model
        
        # First call should load the model
        result = self.service._get_sentence_transformer()
        
        assert result == mock_model
        mock_transformer.assert_called_once_with('all-MiniLM-L6-v2')
    
    @patch('src.services.embedding_service.openai.OpenAI')
    def test_get_openai_client(self, mock_openai):
        """Test lazy loading of OpenAI client."""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # First call should load the client
        result = self.service._get_openai_client()
        
        assert result == mock_client
        mock_openai.assert_called_once()
    
    def test_validate_text_valid(self):
        """Test text validation with valid input."""
        valid_texts = [
            "This is a valid text",
            "Short text",
            "Text with numbers 123 and symbols !@#",
            "A" * 1000  # Long but reasonable text
        ]
        
        for text in valid_texts:
            assert self.service.validate_text(text) is True
    
    def test_validate_text_invalid(self):
        """Test text validation with invalid input."""
        invalid_texts = [
            "",
            None,
            123,
            [],
            {},
            "A" * 10000  # Too long
        ]
        
        for text in invalid_texts:
            assert self.service.validate_text(text) is False
    
    def test_preprocess_text(self):
        """Test text preprocessing."""
        test_cases = [
            ("  hello world  ", "hello world"),
            ("hello\n\nworld", "hello world"),
            ("hello    world", "hello world"),
            ("", ""),
            ("normal text", "normal text")
        ]
        
        for input_text, expected in test_cases:
            result = self.service.preprocess_text(input_text)
            assert result == expected
    
    def test_get_embedding_dimension_sentence_transformers(self):
        """Test embedding dimension for sentence transformers."""
        dimension = self.service.get_embedding_dimension(EmbeddingModel.SENTENCE_TRANSFORMERS)
        assert dimension == 384
    
    def test_get_embedding_dimension_openai_ada(self):
        """Test embedding dimension for OpenAI ADA."""
        dimension = self.service.get_embedding_dimension(EmbeddingModel.OPENAI_ADA)
        assert dimension == 1536
    
    def test_get_embedding_dimension_openai_3_small(self):
        """Test embedding dimension for OpenAI 3 Small."""
        dimension = self.service.get_embedding_dimension(EmbeddingModel.OPENAI_3_SMALL)
        assert dimension == 1536
    
    def test_get_embedding_dimension_openai_3_large(self):
        """Test embedding dimension for OpenAI 3 Large."""
        dimension = self.service.get_embedding_dimension(EmbeddingModel.OPENAI_3_LARGE)
        assert dimension == 3072
    
    def test_get_embedding_dimension_unknown_model(self):
        """Test embedding dimension for unknown model."""
        with pytest.raises(ValueError, match="Unknown model dimension"):
            self.service.get_embedding_dimension("unknown_model")
    
    @patch('src.services.embedding_service.SentenceTransformer')
    def test_generate_sentence_transformer_embedding(self, mock_transformer):
        """Test sentence transformer embedding generation."""
        # Setup mock
        mock_model = Mock()
        mock_embedding = Mock()
        mock_embedding.tolist.return_value = [0.1, 0.2, 0.3]
        mock_model.encode.return_value = mock_embedding
        mock_transformer.return_value = mock_model
        
        # Test embedding generation
        result = self.service._generate_sentence_transformer_embedding("test text")
        
        assert result == [0.1, 0.2, 0.3]
        mock_model.encode.assert_called_once_with("test text", get_unified_utility().convert_to_tensor=False)
    
    @patch('src.services.embedding_service.SentenceTransformer')
    def test_generate_sentence_transformer_batch(self, mock_transformer):
        """Test sentence transformer batch embedding generation."""
        # Setup mock
        mock_model = Mock()
        mock_embeddings = [Mock(), Mock()]
        mock_embeddings[0].tolist.return_value = [0.1, 0.2, 0.3]
        mock_embeddings[1].tolist.return_value = [0.4, 0.5, 0.6]
        mock_model.encode.return_value = mock_embeddings
        mock_transformer.return_value = mock_model
        
        # Test batch embedding generation
        texts = ["text1", "text2"]
        result = self.service._generate_sentence_transformer_batch(texts, batch_size=32)
        
        assert len(result) == 2
        assert result[0] == [0.1, 0.2, 0.3]
        assert result[1] == [0.4, 0.5, 0.6]
        mock_model.encode.assert_called_once_with(texts, batch_size=32, get_unified_utility().convert_to_tensor=False)
    
    @patch('src.services.embedding_service.openai.OpenAI')
    def test_generate_openai_embedding(self, mock_openai):
        """Test OpenAI embedding generation."""
        # Setup mock
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].embedding = [0.1, 0.2, 0.3]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # Test embedding generation
        result = self.service._generate_openai_embedding("test text", EmbeddingModel.OPENAI_ADA)
        
        assert result == [0.1, 0.2, 0.3]
        mock_client.embeddings.create.assert_called_once_with(
            input="test text",
            model="text-embedding-ada-002"
        )
    
    @patch('src.services.embedding_service.openai.OpenAI')
    def test_generate_openai_batch(self, mock_openai):
        """Test OpenAI batch embedding generation."""
        # Setup mock
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [Mock(), Mock()]
        mock_response.data[0].embedding = [0.1, 0.2, 0.3]
        mock_response.data[1].embedding = [0.4, 0.5, 0.6]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # Test batch embedding generation
        texts = ["text1", "text2"]
        result = self.service._generate_openai_batch(texts, EmbeddingModel.OPENAI_ADA)
        
        assert len(result) == 2
        assert result[0] == [0.1, 0.2, 0.3]
        assert result[1] == [0.4, 0.5, 0.6]
        mock_client.embeddings.create.assert_called_once_with(
            input=texts,
            model="text-embedding-ada-002"
        )
    
    @patch.object(EmbeddingService, '_generate_sentence_transformer_embedding')
    def test_generate_embedding_sentence_transformers(self, mock_generate):
        """Test embedding generation with sentence transformers."""
        mock_generate.return_value = [0.1, 0.2, 0.3]
        
        result = self.service.generate_embedding("test text")
        
        assert result == [0.1, 0.2, 0.3]
        mock_generate.assert_called_once_with("test text")
    
    @patch.object(EmbeddingService, '_generate_openai_embedding')
    def test_generate_embedding_openai(self, mock_generate):
        """Test embedding generation with OpenAI."""
        mock_generate.return_value = [0.1, 0.2, 0.3]
        
        result = self.service.generate_embedding("test text", EmbeddingModel.OPENAI_ADA)
        
        assert result == [0.1, 0.2, 0.3]
        mock_generate.assert_called_once_with("test text", EmbeddingModel.OPENAI_ADA)
    
    def test_generate_embedding_unsupported_model(self):
        """Test embedding generation with unsupported model."""
        with pytest.raises(ValueError, match="Unsupported model"):
            self.service.generate_embedding("test text", "unsupported_model")
    
    @patch.object(EmbeddingService, '_generate_sentence_transformer_batch')
    def test_generate_embeddings_batch(self, mock_generate):
        """Test batch embedding generation."""
        mock_generate.return_value = [[0.1, 0.2], [0.3, 0.4]]
        
        texts = ["text1", "text2"]
        result = self.service.generate_embeddings_batch(texts, batch_size=16)
        
        assert result == [[0.1, 0.2], [0.3, 0.4]]
        mock_generate.assert_called_once_with(texts, 16)


if __name__ == "__main__":
    pytest.main([__file__])

