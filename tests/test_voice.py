"""
Unit tests for VoiceService
"""
import pytest
from unittest.mock import Mock, patch
from backend.services.voice import VoiceService


class TestVoiceService:
    """Test cases for VoiceService"""
    
    @pytest.fixture
    def service(self):
        """Create a VoiceService instance with mock API key"""
        with patch.dict('os.environ', {'CARTESIA_API_KEY': 'test_key'}):
            return VoiceService()
    
    def test_init_with_api_key(self):
        """Test initialization with API key"""
        service = VoiceService(api_key='test_key')
        assert service.api_key == 'test_key'
        assert 'X-API-Key' in service.headers
    
    def test_init_without_api_key(self):
        """Test initialization without API key raises ValueError"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError):
                VoiceService()
    
    @patch('backend.services.voice.requests.post')
    def test_generate_audio_success(self, mock_post, service):
        """Test successful audio generation"""
        mock_response = Mock()
        mock_response.content = b'audio_data'
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        result = service.generate_audio("Hello world")
        
        assert result == b'audio_data'
        mock_post.assert_called_once()
    
    @patch('builtins.open', create=True)
    def test_save_audio(self, mock_open, service):
        """Test audio saving to file"""
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        service.save_audio(b'audio_data', '/tmp/test.wav')
        
        mock_file.write.assert_called_once_with(b'audio_data')
    
    @patch('backend.services.voice.requests.post')
    @patch('builtins.open', create=True)
    def test_generate_and_save(self, mock_open, mock_post, service):
        """Test combined generate and save"""
        mock_response = Mock()
        mock_response.content = b'audio_data'
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        result = service.generate_and_save("Hello world", "/tmp/test.wav")
        
        assert result == "/tmp/test.wav"
        mock_post.assert_called_once()
        mock_file.write.assert_called_once()
