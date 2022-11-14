from utils.text.tts_provider import tts_provider


def test_text_to_mp3():
    tts_provider.text_to_mp3("나는 운이 좋았지.다른 사람들은 그렇게 어려운 이별을 한다는데.")
