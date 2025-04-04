import uuid
from edge_tts import Communicate

async def generate_audio(text):
    if not text.strip():
        raise ValueError("Text cannot be empty")

    output_file = f"{str(uuid.uuid4())}.mp3"

    communicate = Communicate(text, voice='pl-PL-ZofiaNeural')
    await communicate.save(output_file)
    return output_file
