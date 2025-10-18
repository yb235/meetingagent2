# Meeting Agent

An AI-powered meeting assistant that can join live meetings, provide real-time transcription and summaries, and handle vocal questions using Recall.ai, Deepgram, OpenAI, and Cartesia.

## Features

- **Meeting Bot**: Automatically join Zoom, Google Meet, and Microsoft Teams meetings
- **Real-time Transcription**: Live transcription using Recall.ai with Deepgram integration
- **AI Summaries**: Generate meeting summaries, extract key points, and identify action items using OpenAI
- **Vocal Questions**: Ask questions in meetings using text-to-speech (Cartesia)
- **Desktop Interface**: Easy-to-use Electron-based desktop application

## Architecture

This is a monorepo with two main components:

```
meeting-agent/
├── backend/          # Python/FastAPI backend
│   ├── services/     # Core services (transcription, AI, voice)
│   ├── api/          # API routes
│   └── main.py       # Application entry point
├── frontend/         # Electron desktop app
│   ├── src/          # UI components
│   └── main.js       # Electron main process
├── shared/           # Shared configurations
├── tests/            # Unit and integration tests
└── docs/             # Documentation
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- API Keys:
  - [Recall.ai](https://docs.recall.ai/) - for bot joining and transcription
  - [OpenAI](https://platform.openai.com/) - for AI processing
  - [Cartesia](https://docs.cartesia.ai/) - for text-to-speech

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/meeting-agent.git
cd meeting-agent
```

### 2. Set up environment variables

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
RECALL_API_KEY=your_recall_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
CARTESIA_API_KEY=your_cartesia_api_key_here
```

### 3. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Install frontend dependencies

```bash
cd ../frontend
npm install
```

## Usage

### Running with Docker (Recommended)

```bash
# Build and start the backend
docker-compose up -d

# In a separate terminal, start the frontend
cd frontend
npm start
```

### Running Locally

#### Start the Backend

```bash
cd backend
python main.py
# or
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

#### Start the Frontend

```bash
cd frontend
npm start
```

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

### Main Endpoints

- `POST /api/v1/join` - Join a meeting
- `GET /api/v1/transcript/{bot_id}` - Get transcript
- `POST /api/v1/summarize` - Generate summary
- `POST /api/v1/generate-question` - Generate a question
- `POST /api/v1/speak` - Generate audio from text
- `POST /api/v1/extract-key-points` - Extract key points
- `POST /api/v1/action-items` - Extract action items

## Development

### Backend Development

The backend uses FastAPI with a modular service architecture:

- **TranscriptionService** (`services/transcription.py`): Handles meeting joining and transcription via Recall.ai
- **AIProcessor** (`services/ai_processor.py`): Processes transcripts with OpenAI
- **VoiceService** (`services/voice.py`): Generates speech using Cartesia

### Frontend Development

The frontend is an Electron desktop application with:
- Clean, modern UI
- Real-time transcript updates
- Meeting controls
- AI-powered features (summaries, questions, key points)

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Project Structure

```
.
├── backend/
│   ├── services/
│   │   ├── __init__.py
│   │   ├── transcription.py    # Recall.ai integration
│   │   ├── ai_processor.py     # OpenAI integration
│   │   └── voice.py            # Cartesia integration
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoints
│   ├── main.py                 # FastAPI application
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── index.html         # Main UI
│   │   ├── styles.css         # Styling
│   │   └── app.js             # Application logic
│   ├── main.js                # Electron main process
│   └── package.json           # Node dependencies
├── .env.example               # Environment variables template
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── package.json               # Root package.json
└── README.md
```

## Key Technologies

- **Backend**: FastAPI, Python 3.11
- **Frontend**: Electron, HTML/CSS/JavaScript
- **APIs**: Recall.ai (meetings), Deepgram (STT), OpenAI (AI), Cartesia (TTS)
- **Deployment**: Docker, Docker Compose

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/meeting-agent/issues)
- Documentation: See the `docs/` folder

## References

- [Recall.ai Documentation](https://docs.recall.ai/)
- [Deepgram Documentation](https://developers.deepgram.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Cartesia Documentation](https://docs.cartesia.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Electron Documentation](https://www.electronjs.org/docs)
