"""
Transcription Service for Meeting Agent
Handles joining meetings and transcribing with Recall.ai + Deepgram
"""
import os
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class TranscriptionService:
    """Service for managing meeting transcription via Recall.ai"""
    
    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        """
        Initialize the transcription service
        
        Args:
            api_key: Recall.ai API key (defaults to env var)
            api_url: Recall.ai API base URL (defaults to env var)
        """
        self.api_key = api_key or os.getenv('RECALL_API_KEY')
        self.api_url = api_url or os.getenv('RECALL_API_URL', 'https://api.recall.ai/api/v1')
        
        if not self.api_key:
            raise ValueError("RECALL_API_KEY must be set in environment or passed to constructor")
        
        self.headers = {
            'Authorization': f'Token {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def join_meeting(self, meeting_url: str, bot_name: str = "Meeting Agent") -> Dict[str, Any]:
        """
        Join a meeting with the bot
        
        Args:
            meeting_url: URL of the meeting to join (Zoom, Google Meet, etc.)
            bot_name: Display name for the bot
            
        Returns:
            Dictionary with bot information including bot_id
            
        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        endpoint = f"{self.api_url}/bot/"
        
        payload = {
            "meeting_url": meeting_url,
            "bot_name": bot_name,
            "transcription_options": {
                "provider": "deepgram",
                "model": "nova-2"
            }
        }
        
        try:
            response = requests.post(endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error joining meeting: {e}")
            raise
    
    def get_transcript(self, bot_id: str) -> Dict[str, Any]:
        """
        Get transcript for a bot
        
        Args:
            bot_id: ID of the bot
            
        Returns:
            Dictionary with transcript data
            
        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        endpoint = f"{self.api_url}/bot/{bot_id}/transcript/"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting transcript: {e}")
            raise
    
    def get_bot_status(self, bot_id: str) -> Dict[str, Any]:
        """
        Get status of a bot
        
        Args:
            bot_id: ID of the bot
            
        Returns:
            Dictionary with bot status information
        """
        endpoint = f"{self.api_url}/bot/{bot_id}/"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting bot status: {e}")
            raise
    
    def leave_meeting(self, bot_id: str) -> Dict[str, Any]:
        """
        Make the bot leave a meeting
        
        Args:
            bot_id: ID of the bot
            
        Returns:
            Dictionary with response data
        """
        endpoint = f"{self.api_url}/bot/{bot_id}/"
        
        try:
            response = requests.delete(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error leaving meeting: {e}")
            raise
