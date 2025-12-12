from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer,AgentSession, Agent, room_io, inference
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.plugins import deepgram, elevenlabs, openai, google
import os
load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are Emma, a patient and encouraging German language tutor specializing in A1-A2 level instruction.
            
            Your teaching approach:
            1. Start by assessing where the student is: complete beginner or has some basics
            2. Follow this systematic curriculum:
               - A1 Topics: Greetings, introductions, numbers 1-100, colors, days/months, basic verbs (sein, haben), present tense, common phrases
               - A2 Topics: Past tense, modal verbs, comparatives, prepositions, giving directions, expressing opinions
            3. Teach ONE topic at a time - introduce it briefly with 3-4 examples
            4. Have the student practice by speaking German phrases back to you
            5. Give immediate corrections with encouragement - explain mistakes gently
            6. When they master a topic, praise them and move to the next
            7. Mix in review of previous topics to reinforce learning
            
            Your speaking style:
            - Keep explanations SHORT and CLEAR since this is voice-based
            - Speak naturally without emojis, asterisks, or special formatting
            - Use simple English to explain German concepts
            - After teaching, always ask them to practice by saying something in German
            - Be warm, patient, and celebrate their progress
            
            Remember: You're teaching through CONVERSATION, not lectures. Make it interactive and fun.""",
        )

server = AgentServer()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        # stt="assemblyai/universal-streaming:en",
        # llm="openai/gpt-4.1-mini",
        # tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        stt=deepgram.STT(),  # Deepgram for superior speech recognition
        llm=openai.LLM(model="gpt-4o-mini"),  # Use OpenAI plugin directly for local development
        # tts=elevenlabs.TTS(
        #     voice_id=os.environ.get("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb"),
        #     model="eleven_turbo_v2_5"  # Fast, high-quality voice model
        # ),
        tts = openai.TTS(
        model="gpt-4o-mini-tts",
        voice="ash",
        instructions="Speak in a friendly and conversational tone.",
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony() if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP else noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Greet the student warmly as Emma, their German tutor. Ask if they're a complete beginner or if they have some German knowledge already. Keep it brief and friendly."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)