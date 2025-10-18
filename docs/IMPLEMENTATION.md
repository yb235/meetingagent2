# Meeting Agent - Detailed Implementation Guide

## Overview

This guide provides detailed information about the implementation of the Meeting Agent, following the architecture outlined in `projectoverview.md` and `implementationprompt`.

## Architecture Decisions

### Monorepo Structure

We chose a monorepo structure for several reasons:
1. **Ease of Development**: Single repository for all components
2. **Simplified Dependencies**: Shared configuration and environment variables
3. **Better Maintenance**: All code in one place for easier updates

### Technology Stack

#### Backend (Python/FastAPI)
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **Python 3.11**: Latest stable version with performance improvements
- **Modular Services**: Separate services for transcription, AI, and voice

#### Frontend (Electron)
- **Electron**: Cross-platform desktop application framework
- **Vanilla JavaScript**: Simple, no framework overhead
- **Modern CSS**: Clean, responsive design

### Service Architecture

#### TranscriptionService
Located in `backend/services/transcription.py`, this service:
- Interfaces with Recall.ai API
- Manages bot lifecycle (join, leave, status)
- Fetches transcripts in real-time
- Uses Deepgram via Recall.ai's native integration

**Key Methods**:
- `join_meeting(meeting_url, bot_name)`: Creates a bot and joins a meeting
- `get_transcript(bot_id)`: Retrieves current transcript
- `get_bot_status(bot_id)`: Checks bot connection status
- `leave_meeting(bot_id)`: Removes bot from meeting

#### AIProcessor
Located in `backend/services/ai_processor.py`, this service:
- Integrates with OpenAI GPT-4o-mini
- Generates summaries from transcripts
- Creates professional questions from user input
- Extracts key points and action items

**Key Methods**:
- `summarize_transcript(transcript, max_sentences)`: Creates concise summaries
- `generate_question(user_input)`: Formats questions professionally
- `extract_key_points(transcript, num_points)`: Identifies main discussion points
- `generate_action_items(transcript)`: Lists actionable tasks

#### VoiceService
Located in `backend/services/voice.py`, this service:
- Integrates with Cartesia TTS API
- Generates natural-sounding speech
- Supports multiple voices and languages
- Returns audio in various formats

**Key Methods**:
- `generate_audio(text, voice, model)`: Creates audio from text
- `save_audio(audio_bytes, filepath)`: Saves audio to file
- `generate_and_save(text, filepath)`: Combined generation and save

## API Design

### RESTful Endpoints

All endpoints are prefixed with `/api/v1/`:

#### Meeting Management
- `POST /join`: Join a meeting
- `DELETE /bot/{bot_id}`: Leave a meeting
- `GET /bot/{bot_id}/status`: Get bot status
- `GET /transcript/{bot_id}`: Get transcript

#### AI Processing
- `POST /summarize`: Generate summary
- `POST /generate-question`: Create question
- `POST /extract-key-points`: Extract key points
- `POST /action-items`: Generate action items

#### Voice
- `POST /speak`: Generate speech audio

### Request/Response Models

Using Pydantic models for validation:
- Type safety
- Automatic validation
- Clear documentation
- Error messages

## Frontend Design

### User Interface

The frontend provides a clean, intuitive interface with:
1. **Meeting Controls**: Join/leave meetings with URL input
2. **Live Transcript**: Real-time transcript display
3. **Summary Generation**: One-click summary creation
4. **Question Input**: Natural language question generation
5. **Key Points/Action Items**: Tabbed interface for insights

### Real-time Updates

- Polling mechanism for transcript updates (5-second intervals)
- Status messages for user feedback
- Responsive UI with loading states

### State Management

Simple state management with:
- Current bot ID tracking
- Transcript caching
- UI state (enabled/disabled buttons)

## Configuration

### Environment Variables

Required variables in `.env`:
```
RECALL_API_KEY=...
OPENAI_API_KEY=...
CARTESIA_API_KEY=...
```

Optional variables:
```
BACKEND_HOST=localhost
BACKEND_PORT=8000
```

### API Keys Setup

1. **Recall.ai**: Sign up at https://recall.ai and get API key
2. **OpenAI**: Create account at https://platform.openai.com
3. **Cartesia**: Register at https://cartesia.ai for TTS access

## Deployment

### Docker Deployment

Using Docker for containerization:
```bash
docker-compose up -d
```

Benefits:
- Isolated environment
- Easy deployment
- Consistent runtime
- Simple scaling

### Local Development

For development:
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm start
```

## Error Handling

### Backend
- Try/except blocks in all service methods
- HTTP exception handling in routes
- Detailed error messages for debugging

### Frontend
- User-friendly error messages
- Status indicators
- Graceful degradation

## Security Considerations

1. **API Keys**: Never commit to repository, use environment variables
2. **CORS**: Configure allowed origins in production
3. **Input Validation**: Pydantic models validate all inputs
4. **Rate Limiting**: Consider adding rate limits for production

## Performance Optimization

1. **Polling**: 5-second interval balances responsiveness and API calls
2. **Model Selection**: GPT-4o-mini for cost-effective processing
3. **Caching**: Transcript caching to reduce API calls
4. **Async Operations**: FastAPI async for better concurrency

## Testing Strategy

### Backend Testing
- Unit tests for each service
- Integration tests for API endpoints
- Mock external APIs for testing

### Frontend Testing
- UI component testing
- API integration testing
- End-to-end testing

## Maintenance

### Code Organization
- Clear separation of concerns
- Modular services
- Well-documented code
- Consistent naming conventions

### Updating Dependencies
```bash
# Backend
pip list --outdated
pip install -U package_name

# Frontend
npm outdated
npm update package_name
```

## Future Enhancements

Potential improvements:
1. WebSocket for real-time transcript streaming
2. Database for transcript storage
3. User authentication
4. Multi-user support
5. Recording playback
6. Advanced analytics
7. Custom voice training
8. Integration with calendar apps

## Troubleshooting

### Common Issues

**Backend won't start**:
- Check Python version (3.11+)
- Verify all dependencies installed
- Check API keys in .env

**Frontend won't connect**:
- Ensure backend is running
- Check CORS configuration
- Verify API_BASE_URL in app.js

**Bot won't join meeting**:
- Verify Recall.ai API key
- Check meeting URL format
- Ensure meeting is accessible

**No transcript appearing**:
- Check bot status endpoint
- Verify meeting has started
- Check Recall.ai dashboard

## Resources

- Implementation Prompt: `implementationprompt`
- Project Overview: `projectoverview.md`
- API References: `reference.md`
