"""
API Routes for Meeting Agent Backend
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from services.transcription import TranscriptionService
from services.ai_processor import AIProcessor
from services.voice import VoiceService

router = APIRouter()

# Initialize services
transcription_service = TranscriptionService()
ai_processor = AIProcessor()
voice_service = VoiceService()


# Request/Response Models
class JoinMeetingRequest(BaseModel):
    meeting_url: str
    bot_name: Optional[str] = "Meeting Agent"


class SummarizeRequest(BaseModel):
    transcript: str
    max_sentences: Optional[int] = 3


class GenerateQuestionRequest(BaseModel):
    user_input: str


class ExtractKeyPointsRequest(BaseModel):
    transcript: str
    num_points: Optional[int] = 5


class GenerateAudioRequest(BaseModel):
    text: str
    voice: Optional[str] = "a0e99841-438c-4a64-b679-ae501e7d6091"


# Transcription Endpoints
@router.post("/join")
async def join_meeting(request: JoinMeetingRequest):
    """Join a meeting with the bot"""
    try:
        result = transcription_service.join_meeting(
            meeting_url=request.meeting_url,
            bot_name=request.bot_name
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transcript/{bot_id}")
async def get_transcript(bot_id: str):
    """Get transcript for a bot"""
    try:
        result = transcription_service.get_transcript(bot_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bot/{bot_id}/status")
async def get_bot_status(bot_id: str):
    """Get status of a bot"""
    try:
        result = transcription_service.get_bot_status(bot_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/bot/{bot_id}")
async def leave_meeting(bot_id: str):
    """Make the bot leave a meeting"""
    try:
        result = transcription_service.leave_meeting(bot_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# AI Processing Endpoints
@router.post("/summarize")
async def summarize_transcript(request: SummarizeRequest):
    """Summarize a transcript"""
    try:
        summary = ai_processor.summarize_transcript(
            transcript=request.transcript,
            max_sentences=request.max_sentences
        )
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-question")
async def generate_question(request: GenerateQuestionRequest):
    """Generate a professional question from user input"""
    try:
        question = ai_processor.generate_question(request.user_input)
        return {"question": question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-key-points")
async def extract_key_points(request: ExtractKeyPointsRequest):
    """Extract key points from a transcript"""
    try:
        points = ai_processor.extract_key_points(
            transcript=request.transcript,
            num_points=request.num_points
        )
        return {"key_points": points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/action-items")
async def generate_action_items(request: SummarizeRequest):
    """Generate action items from a transcript"""
    try:
        items = ai_processor.generate_action_items(request.transcript)
        return {"action_items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Voice Endpoints
@router.post("/speak")
async def generate_audio(request: GenerateAudioRequest):
    """Generate audio from text"""
    try:
        audio_bytes = voice_service.generate_audio(
            text=request.text,
            voice=request.voice
        )
        # Return as base64 or save to file
        import base64
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        return {"audio": audio_base64, "format": "wav"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
