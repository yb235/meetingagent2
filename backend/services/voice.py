"""
Voice Service for Meeting Agent
Handles text-to-speech with Cartesia
"""
import os
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class VoiceService:
    """Service for generating speech using Cartesia TTS"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the voice service
        
        Args:
            api_key: Cartesia API key (defaults to env var)
        """
        self.api_key = api_key or os.getenv('CARTESIA_API_KEY')
        self.api_url = "https://api.cartesia.ai/tts/bytes"
        
        if not self.api_key:
            raise ValueError("CARTESIA_API_KEY must be set in environment or passed to constructor")
        
        self.headers = {
            'X-API-Key': self.api_key,
            'Cartesia-Version': '2024-06-10',
            'Content-Type': 'application/json'
        }
    
    def generate_audio(
        self, 
        text: str, 
        voice: str = "a0e99841-438c-4a64-b679-ae501e7d6091",  # Professional male voice
        model: str = "sonic-english",
        output_format: Dict[str, Any] = None
    ) -> bytes:
        """
        Generate audio from text
        
        Args:
            text: Text to convert to speech
            voice: Voice ID to use (default is professional male)
            model: TTS model to use
            output_format: Audio output format configuration
            
        Returns:
            Audio bytes
            
        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        if output_format is None:
            output_format = {
                "container": "wav",
                "encoding": "pcm_f32le",
                "sample_rate": 44100
            }
        
        payload = {
            "model_id": model,
            "transcript": text,
            "voice": {
                "mode": "id",
                "id": voice
            },
            "output_format": output_format,
            "language": "en"
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error generating audio: {e}")
            raise
    
    def save_audio(self, audio_bytes: bytes, filepath: str) -> None:
        """
        Save audio bytes to file
        
        Args:
            audio_bytes: Audio data to save
            filepath: Path where to save the audio file
        """
        try:
            with open(filepath, 'wb') as f:
                f.write(audio_bytes)
        except Exception as e:
            print(f"Error saving audio: {e}")
            raise
    
    def generate_and_save(self, text: str, filepath: str, **kwargs) -> str:
        """
        Generate audio from text and save to file
        
        Args:
            text: Text to convert to speech
            filepath: Path where to save the audio file
            **kwargs: Additional arguments to pass to generate_audio
            
        Returns:
            Path to saved audio file
        """
        audio_bytes = self.generate_audio(text, **kwargs)
        self.save_audio(audio_bytes, filepath)
        return filepath
