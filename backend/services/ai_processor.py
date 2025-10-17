"""
AI Processor Service for Meeting Agent
Handles summarization and question generation with OpenAI
"""
import os
from typing import Optional, List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class AIProcessor:
    """Service for AI processing using OpenAI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI processor
        
        Args:
            api_key: OpenAI API key (defaults to env var)
        """
        api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError("OPENAI_API_KEY must be set in environment or passed to constructor")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Cost-effective model
    
    def summarize_transcript(self, transcript: str, max_sentences: int = 3) -> str:
        """
        Summarize a meeting transcript
        
        Args:
            transcript: The transcript text to summarize
            max_sentences: Maximum number of sentences in summary
            
        Returns:
            Summarized text
        """
        try:
            prompt = f"Summarize this meeting transcript in {max_sentences} sentences: {transcript}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts concisely."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more focused summaries
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error summarizing transcript: {e}")
            raise
    
    def generate_question(self, user_input: str) -> str:
        """
        Generate a formal meeting question from user input
        
        Args:
            user_input: User's informal question or statement
            
        Returns:
            Formatted question suitable for asking in a meeting
        """
        try:
            prompt = f"Rephrase this as a professional meeting question: {user_input}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that rephrases informal questions into professional meeting questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating question: {e}")
            raise
    
    def extract_key_points(self, transcript: str, num_points: int = 5) -> List[str]:
        """
        Extract key points from a transcript
        
        Args:
            transcript: The transcript text to analyze
            num_points: Number of key points to extract
            
        Returns:
            List of key points
        """
        try:
            prompt = f"Extract {num_points} key points from this meeting transcript: {transcript}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts key points from meeting transcripts. Return the points as a numbered list."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            content = response.choices[0].message.content.strip()
            # Parse numbered list into array
            points = [line.strip() for line in content.split('\n') if line.strip()]
            return points
        except Exception as e:
            print(f"Error extracting key points: {e}")
            raise
    
    def generate_action_items(self, transcript: str) -> List[str]:
        """
        Extract action items from a transcript
        
        Args:
            transcript: The transcript text to analyze
            
        Returns:
            List of action items
        """
        try:
            prompt = f"Extract all action items and next steps from this meeting transcript: {transcript}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that identifies action items from meetings. Return them as a bulleted list with responsible parties if mentioned."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            content = response.choices[0].message.content.strip()
            # Parse list into array
            items = [line.strip() for line in content.split('\n') if line.strip()]
            return items
        except Exception as e:
            print(f"Error generating action items: {e}")
            raise
