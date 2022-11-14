from gtts import gTTS
from django.conf import settings


class TTSProvider:
    def __init__(self) -> None:
        pass

    def text_to_mp3(self, sentence: str, filename: str):
        tts = gTTS(text=sentence, lang="ko", slow=False)
        tts.save(f"{settings.BASE_DIR}/{filename}")


tts_provider = TTSProvider()
