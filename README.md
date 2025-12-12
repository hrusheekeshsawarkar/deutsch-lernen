# Deutsch Lernen - LiveKit Voice AI Agent

A German language learning application powered by LiveKit voice agents.

## Project Structure

- **livekit-voice-agent/** - Python-based voice AI agent using LiveKit, OpenAI, Deepgram, and ElevenLabs
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

- 🎤 Real-time voice interaction
- 🗣️ Deepgram speech-to-text
- 🤖 OpenAI GPT-4o-mini for conversation
- 🔊 ElevenLabs text-to-speech
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

