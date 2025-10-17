# Meeting Agent - Quick Start Guide

## Overview

This Meeting Agent is a complete AI-powered solution for managing virtual meetings. It can:
- Join meetings automatically (Zoom, Google Meet, Teams)
- Provide real-time transcription
- Generate summaries and extract key points
- Ask questions using text-to-speech
- Identify action items

## 5-Minute Quick Start

### Prerequisites

1. **API Keys**: You'll need:
   - [Recall.ai](https://recall.ai) API key
   - [OpenAI](https://platform.openai.com) API key
   - [Cartesia](https://cartesia.ai) API key

2. **Software**:
   - Python 3.11+ or Docker
   - Node.js 18+ (for frontend)

### Setup

1. **Clone and Configure**:
   ```bash
   git clone <repository-url>
   cd meetingagent2
   cp .env.example .env
   # Edit .env and add your API keys
   ```

2. **Run with Docker** (Recommended):
   ```bash
   # Start backend
   docker-compose up -d
   
   # In a new terminal, start frontend
   cd frontend
   npm install
   npm start
   ```

3. **OR Run Locally**:
   ```bash
   # Terminal 1 - Backend
   cd backend
   pip install -r requirements.txt
   python main.py
   
   # Terminal 2 - Frontend
   cd frontend
   npm install
   npm start
   ```

### Using the Application

1. **Join a Meeting**:
   - Enter the meeting URL (Zoom, Google Meet, or Teams)
   - Click "Join Meeting"
   - The bot will join and start transcribing

2. **View Transcript**:
   - Live transcript appears automatically
   - Updates every 5 seconds

3. **Generate Summary**:
   - Click "Generate Summary" to get a concise overview
   - Summaries are created using AI

4. **Ask Questions**:
   - Type your question in the text box
   - Click "Ask Question"
   - The AI will rephrase it professionally and generate audio

5. **Extract Insights**:
   - Click "Extract Key Points" for main discussion topics
   - Click "Extract Action Items" for tasks and next steps

## Architecture at a Glance

```
┌─────────────────┐
│  Electron UI    │  ← User Interface
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Backend│  ← RESTful API
└────────┬────────┘
         │
    ┌────┴────┬─────────┬──────────┐
    ▼         ▼         ▼          ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌─────────┐
│Recall  │ │OpenAI│ │Deepgram│ │Cartesia │
│.ai     │ │      │ │(via    │ │TTS      │
│        │ │      │ │Recall) │ │         │
└────────┘ └──────┘ └────────┘ └─────────┘
```

## Project Structure

```
meetingagent2/
├── backend/              # Python/FastAPI backend
│   ├── services/        # Core services
│   │   ├── transcription.py   # Meeting joining & transcription
│   │   ├── ai_processor.py    # AI summarization & questions
│   │   └── voice.py           # Text-to-speech
│   ├── api/routes.py    # API endpoints
│   └── main.py          # Application entry
├── frontend/            # Electron desktop app
│   ├── src/
│   │   ├── index.html   # UI
│   │   ├── styles.css   # Styling
│   │   └── app.js       # Application logic
│   └── main.js          # Electron main
├── docs/                # Documentation
├── tests/               # Unit tests
└── README.md            # Main documentation
```

## Key Features

### Backend Services

1. **TranscriptionService**:
   - Interfaces with Recall.ai
   - Manages bot lifecycle
   - Fetches real-time transcripts

2. **AIProcessor**:
   - Summarizes transcripts
   - Generates professional questions
   - Extracts key points and action items

3. **VoiceService**:
   - Converts text to natural speech
   - Supports multiple voices

### API Endpoints

All endpoints are prefixed with `/api/v1`:
- `POST /join` - Join meeting
- `GET /transcript/{bot_id}` - Get transcript
- `POST /summarize` - Generate summary
- `POST /generate-question` - Create question
- `POST /speak` - Generate audio
- `POST /extract-key-points` - Extract insights
- `POST /action-items` - Get action items

### Frontend Features

- Clean, modern UI
- Real-time updates
- Easy-to-use controls
- Status indicators
- Tabbed interface for insights

## Documentation

- **README.md** - Main documentation and setup
- **docs/API.md** - Complete API reference
- **docs/IMPLEMENTATION.md** - Detailed implementation guide
- **projectoverview.md** - Architecture overview
- **reference.md** - External references

## Testing

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run tests
pytest tests/ -v
```

## Troubleshooting

**Backend won't start?**
- Check Python version (3.11+)
- Verify API keys in `.env`
- Check port 8000 is available

**Frontend won't connect?**
- Ensure backend is running
- Check console for errors
- Verify `API_BASE_URL` in `frontend/src/app.js`

**Bot won't join?**
- Verify Recall.ai API key
- Check meeting URL format
- Ensure meeting is accessible

## Security

✅ **Security Scan**: No vulnerabilities detected
- All API keys stored in environment variables
- Input validation using Pydantic
- CORS configured for security
- No secrets in code

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run tests
5. Submit pull request

## Support

- GitHub Issues for bug reports
- Documentation in `/docs` folder
- API documentation at `/docs` endpoint (when backend is running)

## License

MIT

---

**Ready to start?** Just follow the 5-minute quick start above!
