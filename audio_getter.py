from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs
import io
from moviepy.editor import *
import tempfile
import transcriber

# Keys I found on github
# ----------------------
# sk_02c02e595901fe869a0db07bfceac0ad188ccf5d55da133d
# sk_68b4b42e8e8da72a711bbda6ab3be505a604241d3d585901
# sk_e77d0b46b544dcba9956594fd17f40b67b8cd83422933c9e

CLIENT = ElevenLabs(api_key="sk_e77d0b46b544dcba9956594fd17f40b67b8cd83422933c9e")

class AudioGetter:
    def get_audio(self, message = str, voice_id = 'pNInz6obpgDQGcFmaJgB'):
        audio = CLIENT.generate(
            text=message,
            voice=Voice(
                voice_id=voice_id,
                settings=VoiceSettings(stability=1.0, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
            )
        )
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio_file:
            for data in audio:
                temp_audio_file.write(data)
            temp_audio_file.seek(0)
        return temp_audio_file.name
    def comp_audio(self, txt):
        import math
        
        clips = []
        for i in range(math.ceil(len(txt)/1999)):
            message = txt[i * 1999: len(txt) if len(txt) < 1999 else (1+i) * 1999]
            audio = self.get_audio(message)
            clips.append(AudioFileClip(audio))

        return concatenate_audioclips(clips)
