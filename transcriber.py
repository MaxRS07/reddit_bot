from faster_whisper import WhisperModel
from moviepy.editor import *
import tempfile
import io
from utils import save_temp, encode_image

DUBDUB = "KEY"
KEY = "APIKEY"
KEY2 = "APIKEY"
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
