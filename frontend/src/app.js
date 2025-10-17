// Meeting Agent Frontend Application

const API_BASE_URL = 'http://localhost:8000/api/v1';

// State
let currentBotId = null;
let currentTranscript = '';

// DOM Elements
const joinBtn = document.getElementById('join-btn');
const leaveBtn = document.getElementById('leave-btn');
const meetingUrlInput = document.getElementById('meeting-url');
const botNameInput = document.getElementById('bot-name');
const statusDiv = document.getElementById('status');
const transcriptArea = document.getElementById('transcript-area');
const summarizeBtn = document.getElementById('summarize-btn');
const summaryArea = document.getElementById('summary-area');
const questionInput = document.getElementById('question-input');
const askBtn = document.getElementById('ask-btn');
const generatedQuestionDiv = document.getElementById('generated-question');
const extractPointsBtn = document.getElementById('extract-points-btn');
const extractActionsBtn = document.getElementById('extract-actions-btn');
const keyPointsList = document.getElementById('key-points-list');
const actionItemsList = document.getElementById('action-items-list');

// Event Listeners
joinBtn.addEventListener('click', joinMeeting);
leaveBtn.addEventListener('click', leaveMeeting);
summarizeBtn.addEventListener('click', generateSummary);
askBtn.addEventListener('click', askQuestion);
extractPointsBtn.addEventListener('click', extractKeyPoints);
extractActionsBtn.addEventListener('click', extractActionItems);

// Tab functionality
const tabButtons = document.querySelectorAll('.tab-btn');
tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        switchTab(tabName);
    });
});

function switchTab(tabName) {
    // Remove active class from all tabs and buttons
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Add active class to selected tab
    document.getElementById(tabName).classList.add('active');
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
}

// Utility function to show status messages
function showStatus(message, type = 'info') {
    statusDiv.textContent = message;
    statusDiv.className = `status-message ${type}`;
}

// Join Meeting
async function joinMeeting() {
    const meetingUrl = meetingUrlInput.value.trim();
    const botName = botNameInput.value.trim() || 'Meeting Agent';
    
    if (!meetingUrl) {
        showStatus('Please enter a meeting URL', 'error');
        return;
    }
    
    try {
        joinBtn.disabled = true;
        showStatus('Joining meeting...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/join`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                meeting_url: meetingUrl,
                bot_name: botName
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to join meeting');
        }
        
        const data = await response.json();
        currentBotId = data.id;
        
        showStatus('Successfully joined meeting!', 'success');
        leaveBtn.disabled = false;
        summarizeBtn.disabled = false;
        askBtn.disabled = false;
        extractPointsBtn.disabled = false;
        extractActionsBtn.disabled = false;
        
        // Start polling for transcript
        startTranscriptPolling();
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
        joinBtn.disabled = false;
    }
}

// Leave Meeting
async function leaveMeeting() {
    if (!currentBotId) return;
    
    try {
        leaveBtn.disabled = true;
        showStatus('Leaving meeting...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/bot/${currentBotId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to leave meeting');
        }
        
        showStatus('Left meeting successfully', 'success');
        resetUI();
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
        leaveBtn.disabled = false;
    }
}

// Poll for transcript updates
let transcriptPollingInterval = null;

function startTranscriptPolling() {
    if (transcriptPollingInterval) {
        clearInterval(transcriptPollingInterval);
    }
    
    transcriptPollingInterval = setInterval(async () => {
        if (!currentBotId) {
            clearInterval(transcriptPollingInterval);
            return;
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}/transcript/${currentBotId}`);
            if (response.ok) {
                const data = await response.json();
                if (data.transcript) {
                    updateTranscript(data.transcript);
                }
            }
        } catch (error) {
            console.error('Error fetching transcript:', error);
        }
    }, 5000); // Poll every 5 seconds
}

function updateTranscript(transcript) {
    currentTranscript = transcript;
    transcriptArea.innerHTML = `<p>${transcript.replace(/\n/g, '<br>')}</p>`;
}

// Generate Summary
async function generateSummary() {
    if (!currentTranscript) {
        showStatus('No transcript available to summarize', 'error');
        return;
    }
    
    try {
        summarizeBtn.disabled = true;
        showStatus('Generating summary...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/summarize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                transcript: currentTranscript,
                max_sentences: 3
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate summary');
        }
        
        const data = await response.json();
        summaryArea.innerHTML = `<p><strong>Summary:</strong></p><p>${data.summary}</p>`;
        showStatus('Summary generated successfully', 'success');
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        summarizeBtn.disabled = false;
    }
}

// Ask Question
async function askQuestion() {
    const userInput = questionInput.value.trim();
    
    if (!userInput) {
        showStatus('Please enter a question', 'error');
        return;
    }
    
    try {
        askBtn.disabled = true;
        showStatus('Generating question...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/generate-question`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_input: userInput
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate question');
        }
        
        const data = await response.json();
        generatedQuestionDiv.innerHTML = `<p><strong>Generated Question:</strong></p><p>${data.question}</p>`;
        generatedQuestionDiv.classList.add('show');
        
        // Generate audio for the question
        await generateAudio(data.question);
        
        showStatus('Question generated successfully', 'success');
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        askBtn.disabled = false;
    }
}

// Generate Audio
async function generateAudio(text) {
    try {
        const response = await fetch(`${API_BASE_URL}/speak`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            // Audio is returned as base64, could be played or sent to meeting
            console.log('Audio generated successfully');
        }
    } catch (error) {
        console.error('Error generating audio:', error);
    }
}

// Extract Key Points
async function extractKeyPoints() {
    if (!currentTranscript) {
        showStatus('No transcript available', 'error');
        return;
    }
    
    try {
        extractPointsBtn.disabled = true;
        showStatus('Extracting key points...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/extract-key-points`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                transcript: currentTranscript,
                num_points: 5
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to extract key points');
        }
        
        const data = await response.json();
        const pointsHtml = data.key_points.map(point => `<p>• ${point}</p>`).join('');
        keyPointsList.innerHTML = pointsHtml;
        showStatus('Key points extracted successfully', 'success');
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        extractPointsBtn.disabled = false;
    }
}

// Extract Action Items
async function extractActionItems() {
    if (!currentTranscript) {
        showStatus('No transcript available', 'error');
        return;
    }
    
    try {
        extractActionsBtn.disabled = true;
        showStatus('Extracting action items...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/action-items`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                transcript: currentTranscript
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to extract action items');
        }
        
        const data = await response.json();
        const itemsHtml = data.action_items.map(item => `<p>• ${item}</p>`).join('');
        actionItemsList.innerHTML = itemsHtml;
        showStatus('Action items extracted successfully', 'success');
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        extractActionsBtn.disabled = false;
    }
}

// Reset UI
function resetUI() {
    currentBotId = null;
    currentTranscript = '';
    joinBtn.disabled = false;
    leaveBtn.disabled = true;
    summarizeBtn.disabled = true;
    askBtn.disabled = true;
    extractPointsBtn.disabled = true;
    extractActionsBtn.disabled = true;
    transcriptArea.innerHTML = '<p class="placeholder">Transcript will appear here once the meeting starts...</p>';
    summaryArea.innerHTML = '';
    generatedQuestionDiv.classList.remove('show');
    keyPointsList.innerHTML = '<p class="placeholder">Key points will appear here...</p>';
    actionItemsList.innerHTML = '<p class="placeholder">Action items will appear here...</p>';
    
    if (transcriptPollingInterval) {
        clearInterval(transcriptPollingInterval);
    }
}
