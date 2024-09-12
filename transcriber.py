from faster_whisper import WhisperModel
from moviepy.editor import *
import tempfile
import io
from utils import save_temp, encode_image

DUBDUB = "5244d18eaf3a4eb3a7b150ff3615c435"
KEY = "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"
KEY2 = "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"
def generate(audio=AudioFileClip):
    model_size = "small"

    model = WhisperModel(model_size, device="cpu", compute_type="int8")


    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
        temp_filename = temp_file.name
        temp_file.close()

    audio.write_audiofile(temp_filename)

    segments, info = model.transcribe(temp_filename, beam_size=5, word_timestamps=True)
    
    result = []
    for segment in segments:
        for word in segment.words:
            result.append(((word.start, word.end), word.word))
    
    return result

def create_script(video=VideoFileClip):
    samples = 5
    length = video.duration
    frames = []
    for i in range(samples):
        t = length * i / samples
        frame = video.get_frame(t)
        frames.append(frame)
    images = []
    for frame in frames:
        im = save_temp(frame)
        images.append(im)