"""
Unit tests for TranscriptionService
"""
import pytest
from unittest.mock import Mock, patch
from backend.services.transcription import TranscriptionService


class TestTranscriptionService:
    """Test cases for TranscriptionService"""
    
    @pytest.fixture
    def service(self):
        """Create a TranscriptionService instance with mock API key"""
        with patch.dict('os.environ', {'RECALL_API_KEY': 'test_key'}):
            return TranscriptionService()
    
    def test_init_with_api_key(self):
        """Test initialization with API key"""
        service = TranscriptionService(api_key='test_key')
        assert service.api_key == 'test_key'
        assert 'Authorization' in service.headers
    
    def test_init_without_api_key(self):
        """Test initialization without API key raises ValueError"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError):
                TranscriptionService()
    
    @patch('backend.services.transcription.requests.post')
    def test_join_meeting_success(self, mock_post, service):
        """Test successful meeting join"""
        mock_response = Mock()
        mock_response.json.return_value = {'id': 'bot_123', 'status': 'joining'}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        result = service.join_meeting('https://zoom.us/j/123456789')
        
        assert result['id'] == 'bot_123'
        assert result['status'] == 'joining'
        mock_post.assert_called_once()
    
    @patch('backend.services.transcription.requests.get')
    def test_get_transcript_success(self, mock_get, service):
        """Test successful transcript retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = {'transcript': 'Hello world'}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = service.get_transcript('bot_123')
        
        assert result['transcript'] == 'Hello world'
        mock_get.assert_called_once()
    
    @patch('backend.services.transcription.requests.get')
    def test_get_bot_status_success(self, mock_get, service):
        """Test successful bot status retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = {'id': 'bot_123', 'status': 'in_meeting'}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = service.get_bot_status('bot_123')
        
        assert result['status'] == 'in_meeting'
        mock_get.assert_called_once()
    
    @patch('backend.services.transcription.requests.delete')
    def test_leave_meeting_success(self, mock_delete, service):
        """Test successful meeting leave"""
        mock_response = Mock()
        mock_response.json.return_value = {'success': True}
        mock_response.raise_for_status = Mock()
        mock_delete.return_value = mock_response
        
        result = service.leave_meeting('bot_123')
        
        assert result['success'] is True
        mock_delete.assert_called_once()
