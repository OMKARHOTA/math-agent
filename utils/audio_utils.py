import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path: str):

    result = model.transcribe(audio=audio_path)

    text = result["text"].strip()

    return text