"""
Unit tests for AIProcessor
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.services.ai_processor import AIProcessor


class TestAIProcessor:
    """Test cases for AIProcessor"""
    
    @pytest.fixture
    def processor(self):
        """Create an AIProcessor instance with mock API key"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
            return AIProcessor()
    
    def test_init_with_api_key(self):
        """Test initialization with API key"""
        with patch('backend.services.ai_processor.OpenAI') as mock_openai:
            processor = AIProcessor(api_key='test_key')
            mock_openai.assert_called_once_with(api_key='test_key')
    
    def test_init_without_api_key(self):
        """Test initialization without API key raises ValueError"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError):
                AIProcessor()
    
    def test_summarize_transcript(self, processor):
        """Test transcript summarization"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "This is a summary."
        processor.client.chat.completions.create = Mock(return_value=mock_response)
        
        result = processor.summarize_transcript("Long transcript here...")
        
        assert result == "This is a summary."
        processor.client.chat.completions.create.assert_called_once()
    
    def test_generate_question(self, processor):
        """Test question generation"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Could you please clarify the status?"
        processor.client.chat.completions.create = Mock(return_value=mock_response)
        
        result = processor.generate_question("what's the status")
        
        assert "status" in result.lower()
        processor.client.chat.completions.create.assert_called_once()
    
    def test_extract_key_points(self, processor):
        """Test key points extraction"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "1. Point one\n2. Point two\n3. Point three"
        processor.client.chat.completions.create = Mock(return_value=mock_response)
        
        result = processor.extract_key_points("Transcript with key points...")
        
        assert len(result) == 3
        processor.client.chat.completions.create.assert_called_once()
    
    def test_generate_action_items(self, processor):
        """Test action items generation"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "- John: Complete report\n- Sarah: Review document"
        processor.client.chat.completions.create = Mock(return_value=mock_response)
        
        result = processor.generate_action_items("Transcript with action items...")
        
        assert len(result) == 2
        processor.client.chat.completions.create.assert_called_once()
