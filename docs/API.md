# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All API endpoints require appropriate API keys to be configured in the backend environment variables. The frontend does not need to pass authentication headers.

## Endpoints

### Health Check

#### GET /health

Check if the API is running.

**Response**:
```json
{
  "status": "healthy"
}
```

---

### Meeting Management

#### POST /api/v1/join

Join a meeting with the bot.

**Request Body**:
```json
{
  "meeting_url": "https://zoom.us/j/123456789",
  "bot_name": "Meeting Agent"
}
```

**Response**:
```json
{
  "id": "bot_abc123",
  "meeting_url": "https://zoom.us/j/123456789",
  "bot_name": "Meeting Agent",
  "status": "joining"
}
```

#### GET /api/v1/transcript/{bot_id}

Get the current transcript for a bot.

**Parameters**:
- `bot_id` (path): ID of the bot

**Response**:
```json
{
  "transcript": "Hello everyone, let's start the meeting...",
  "words": [...]
}
```

#### GET /api/v1/bot/{bot_id}/status

Get the current status of a bot.

**Parameters**:
- `bot_id` (path): ID of the bot

**Response**:
```json
{
  "id": "bot_abc123",
  "status": "in_meeting",
  "meeting_url": "https://zoom.us/j/123456789"
}
```

#### DELETE /api/v1/bot/{bot_id}

Make the bot leave the meeting.

**Parameters**:
- `bot_id` (path): ID of the bot

**Response**:
```json
{
  "success": true,
  "message": "Bot left meeting successfully"
}
```

---

### AI Processing

#### POST /api/v1/summarize

Generate a summary from a transcript.

**Request Body**:
```json
{
  "transcript": "The meeting discussed Q3 results and planning for Q4...",
  "max_sentences": 3
}
```

**Response**:
```json
{
  "summary": "The team reviewed Q3 performance metrics. Key achievements include 20% revenue growth. Q4 planning will focus on market expansion."
}
```

#### POST /api/v1/generate-question

Generate a professional question from user input.

**Request Body**:
```json
{
  "user_input": "what's the status"
}
```

**Response**:
```json
{
  "question": "Could you please provide an update on the current status?"
}
```

#### POST /api/v1/extract-key-points

Extract key points from a transcript.

**Request Body**:
```json
{
  "transcript": "We discussed the project timeline, budget constraints...",
  "num_points": 5
}
```

**Response**:
```json
{
  "key_points": [
    "1. Project timeline extended by 2 weeks",
    "2. Budget constraints require reallocation",
    "3. Team size will increase by 3 members",
    "4. Client presentation scheduled for next week",
    "5. Technical challenges identified in phase 2"
  ]
}
```

#### POST /api/v1/action-items

Extract action items from a transcript.

**Request Body**:
```json
{
  "transcript": "John will prepare the report. Sarah needs to contact the client..."
}
```

**Response**:
```json
{
  "action_items": [
    "- John: Prepare the quarterly report by Friday",
    "- Sarah: Contact client regarding contract renewal",
    "- Team: Review updated documentation before next meeting"
  ]
}
```

---

### Voice

#### POST /api/v1/speak

Generate audio from text using TTS.

**Request Body**:
```json
{
  "text": "Could you please provide an update on the current status?",
  "voice": "a0e99841-438c-4a64-b679-ae501e7d6091"
}
```

**Response**:
```json
{
  "audio": "base64_encoded_audio_data...",
  "format": "wav"
}
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- `400`: Bad Request - Invalid input
- `404`: Not Found - Resource not found
- `500`: Internal Server Error - Server-side error

## Rate Limits

Currently no rate limits are enforced, but consider implementing them for production use.

## Examples

### cURL Examples

**Join a meeting**:
```bash
curl -X POST http://localhost:8000/api/v1/join \
  -H "Content-Type: application/json" \
  -d '{"meeting_url": "https://zoom.us/j/123456789", "bot_name": "My Bot"}'
```

**Get transcript**:
```bash
curl http://localhost:8000/api/v1/transcript/bot_abc123
```

**Generate summary**:
```bash
curl -X POST http://localhost:8000/api/v1/summarize \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Meeting transcript here...", "max_sentences": 3}'
```

### JavaScript Examples

**Join a meeting**:
```javascript
const response = await fetch('http://localhost:8000/api/v1/join', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    meeting_url: 'https://zoom.us/j/123456789',
    bot_name: 'Meeting Agent'
  })
});
const data = await response.json();
console.log(data);
```

**Generate summary**:
```javascript
const response = await fetch('http://localhost:8000/api/v1/summarize', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    transcript: 'Meeting transcript...',
    max_sentences: 3
  })
});
const data = await response.json();
console.log(data.summary);
```
