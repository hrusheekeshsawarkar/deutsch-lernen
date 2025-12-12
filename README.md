# Deutsch Lernen - AI German Language Tutor

An interactive German language learning application powered by LiveKit voice AI. Practice speaking German with Emma, your AI tutor who systematically teaches A1-A2 level German through conversation.

## How It Works

Meet **Emma**, your AI German tutor! She'll guide you through German learning with this approach:

1. **Assessment** - Emma first asks about your current level (complete beginner or some basics)
2. **Structured Curriculum**:
   - **A1 Level**: Greetings, introductions, numbers, colors, days/months, basic verbs (sein, haben), present tense
   - **A2 Level**: Past tense, modal verbs, comparatives, prepositions, directions, expressing opinions
3. **Interactive Practice** - Learn one topic, then practice it by speaking German
4. **Immediate Feedback** - Get gentle corrections and explanations in real-time
5. **Progress & Review** - Master topics before moving forward, with regular review

**Example session:**
```
Emma: "Hello! I'm Emma, your German tutor. Are you a complete beginner or do you have some German knowledge?"
You: "I'm a complete beginner"
Emma: "Perfect! Let's start with greetings. In German, hello is 'Hallo', good morning is 'Guten Morgen'..."
```

## Project Structure

- **livekit-voice-agent/** - Python-based voice AI tutor using LiveKit, OpenAI, and Deepgram
- **lk-ui/** - Next.js web interface for the voice agent

## Quick Start

```bash
# 1. Install LiveKit server
brew install livekit  # macOS

# 2. Setup backend
cd livekit-voice-agent
uv sync  # Install Python dependencies
# Add your API keys to .env.local

# 3. Setup frontend
cd ../lk-ui
pnpm install  # Install Node.js dependencies

# 4. Run everything (3 terminals)
# Terminal 1: LiveKit server
livekit-server --dev

# Terminal 2: Voice agent (auto-downloads models on first run)
cd livekit-voice-agent && uv run agent.py dev

# Terminal 3: Frontend
cd lk-ui && pnpm dev
# Open http://localhost:3000
```

## Prerequisites

- Python 3.13+
- Node.js 18+
- [uv](https://github.com/astral-sh/uv) package manager
- LiveKit Server (for local development)

## Setup

### 1. Install LiveKit Server (Backend)

**macOS (using Homebrew):**
```bash
brew install livekit
```

**Linux:**
```bash
curl -sSL https://get.livekit.io | bash
```

**Windows:**
Download from [LiveKit Releases](https://github.com/livekit/livekit/releases)

**Verify installation:**
```bash
livekit-server --version
```

### 2. Setup Backend (Python Agent)

**Install Python dependencies using uv:**
```bash
cd livekit-voice-agent
uv sync
```

**Download AI models:**

The first time you run the agent, it will automatically download the required models:
- Silero VAD model (voice activity detection)
- Multilingual turn detection model

This happens automatically on first run, but you can trigger it manually:
```bash
uv run agent.py console
# Press Ctrl+C after models are downloaded
```

### 3. Setup Frontend (Next.js UI)

**Install Node.js dependencies:**
```bash
cd lk-ui
pnpm install
# If you don't have pnpm: npm install -g pnpm
```

**Configure frontend environment:**

Create a `.env.local` file in the `lk-ui/` directory:
```bash
NEXT_PUBLIC_LIVEKIT_URL=ws://localhost:7880
```

### 4. Configure Environment Variables

Create a `.env.local` file in the `livekit-voice-agent/` directory:

```bash
# LiveKit Server Configuration (local)
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
NEXT_PUBLIC_LIVEKIT_URL=ws://localhost:7880

# API Keys
OPENAI_API_KEY=your_openai_api_key
ELEVEN_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_voice_id
DEEPGRAM_API_KEY=your_deepgram_api_key
```

⚠️ **Never commit `.env.local` to version control!**

## Running Locally

You'll need **three terminal windows** running simultaneously:

### Terminal 1: Start LiveKit Server (Backend)

```bash
livekit-server --dev
```

The server will run on `ws://localhost:7880` with default dev credentials (`devkey`/`secret`).

**Expected output:**
```
INFO    Starting LiveKit server
INFO    Server listening on :7880
```

### Terminal 2: Start the Voice Agent (Backend)

```bash
cd livekit-voice-agent
uv run agent.py dev
```

This will start the Python agent and download AI models on first run (Silero VAD, multilingual turn detector).

**Expected output:**
```
INFO    livekit.agents     registered worker {"url": "ws://localhost:7880"}
```

### Terminal 3: Start the Frontend

**Option A: Simple HTML Test Client (Need to work on this, not working currently, Quick Test)**
```bash
open livekit-voice-agent/test_client.html
```

**Option B: Next.js UI (Full Featured)**
```bash
cd lk-ui
pnpm dev
```

Then open http://localhost:3000 in your browser.

**Note:** Allow microphone access when prompted, then start speaking to interact with the AI assistant!

## Features

### Language Learning
- 📚 **Systematic A1-A2 German curriculum** - Structured progression from basics to intermediate
- 🎓 **Interactive lessons** - Learn through natural conversation, not lectures
- 🗣️ **Speaking practice** - Practice pronunciation and get immediate feedback
- ✅ **Instant corrections** - Gentle guidance when you make mistakes
- 🎯 **One topic at a time** - Master each concept before moving forward
- 🔄 **Progressive review** - Reinforce previous lessons while learning new material

### Technical Features
- 🎤 Real-time voice interaction with low latency
- 🗣️ Deepgram speech-to-text for accurate voice recognition
- 🤖 OpenAI GPT-4o-mini powered AI tutor
- 🔊 Natural text-to-speech voice
- 🎯 Voice activity detection (Silero VAD)
- 🌍 Multilingual turn detection
- 🎨 Modern Next.js UI

## Development

### Running Agent in Console Mode

For testing without a web interface:

```bash
cd livekit-voice-agent
uv run agent.py console
```

### Using with LiveKit Cloud

To use LiveKit Cloud instead of local server, update `.env.local`:

```bash
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
```

## Architecture

```
┌─────────────┐     WebRTC       ┌──────────────────┐
│   Browser   │ ◄──────────────► │ LiveKit Server   │
│  (Client)   │                  │  (localhost:7880)│
└─────────────┘                  └──────────────────┘
                                          │
                                    WebSocket
                                          │
                                  ┌───────▼────────┐
                                  │  Voice Agent   │
                                  │   (Python)     │
                                  └────────────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    ▼                     ▼                     ▼
              ┌──────────┐          ┌─────────┐          ┌──────────┐
              │ Deepgram │          │ OpenAI  │          │ElevenLabs│
              │   (STT)  │          │  (LLM)  │          │  (TTS)   │
              └──────────┘          └─────────┘          └──────────┘
```

## Troubleshooting

### Agent not connecting
- Ensure LiveKit server is running: `livekit-server --dev`
- Check `.env.local` has correct server URL and credentials
- Verify no other service is using port 7880

### No audio
- Check browser permissions for microphone
- Ensure ElevenLabs API key is valid
- Check browser console for WebRTC errors

### 401 Errors
- If seeing "object cannot be found" errors, ensure you're using `openai.LLM()` directly instead of the inference API shorthand when running locally

## License

MIT

## Resources

- [LiveKit Documentation](https://docs.livekit.io/)
- [LiveKit Agents Guide](https://docs.livekit.io/agents/start/voice-ai/)
- [LiveKit Self-Hosting](https://docs.livekit.io/home/self-hosting/local/)

