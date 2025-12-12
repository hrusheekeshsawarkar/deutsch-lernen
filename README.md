# Deutsch Lernen - LiveKit Voice AI Agent

A German language learning application powered by LiveKit voice agents.

## Project Structure

- **livekit-voice-agent/** - Python-based voice AI agent using LiveKit, OpenAI, Deepgram, and ElevenLabs
- **lk-ui/** - Next.js web interface for the voice agent

## Prerequisites

- Python 3.13+
- Node.js 18+
- [uv](https://github.com/astral-sh/uv) package manager
- LiveKit Server (for local development)

## Setup

### 1. Environment Variables

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

### 2. Install Dependencies

**Python Agent:**
```bash
cd livekit-voice-agent
uv sync
```

**Next.js UI:**
```bash
cd lk-ui
pnpm install
```

## Running Locally

### 1. Start LiveKit Server

```bash
livekit-server --dev
```

The server will run on `ws://localhost:7880` with default dev credentials.

### 2. Start the Voice Agent

```bash
cd livekit-voice-agent
uv run agent.py dev
```

### 3. Test with the Web Client

**Option A: Simple HTML Test Client**
```bash
open livekit-voice-agent/test_client.html
```

**Option B: Next.js UI**
```bash
cd lk-ui
pnpm dev
```

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

