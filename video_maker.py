from moviepy.editor import *
from moviepy.tools import *
from reddit_getter import *
from PIL import Image
import random
import numpy as np
from utils import *
from audio_getter import *
from moviepy.config import change_settings

class VideoEditor: 
    def __init__(self, video=VideoFileClip):
        self.video = video
    def resize(self, ratio=float(9/16)):
        height = self.video.size[1]
        width = int(height * ratio)
        cropped = self.video.subclip(0, None).crop(x1=width, y1=0, x2=width*2, y2=height)
        return VideoEditor(cropped)
    def trim(self, start=0, end=0):
        trimmed_clip = self.video.subclip(start, end)
        return VideoEditor(trimmed_clip)
    def random_trim(self, duration=-1):
        rand = random.Random()
        max = self.video.duration
        start = rand.randrange(0, int(max))
        end = start + duration if duration != -1 else self.video.duration
        trimmed_clip = self.video.subclip(start, end)
        return VideoEditor(trimmed_clip)
    def composite_audio(self, audio):
        new_audioclip = CompositeAudioClip([audio])
        self.video.audio = new_audioclip
        return VideoEditor(self.video)
    def composite_text(self, segments = list, offset=float):
        width, height = self.video.size
        text = []
        for (start, stop), phrase in join_words(segments, 4):
            brokentext = break_text(phrase)
            r = random.randrange(0, 5)
            color = "white"
            if r == 2:
                color = "yellow"
            clip = TextClip(brokentext, fontsize=28, font="SF-Compact-Rounded-Medium", color=color,size=(width, height)).set_duration(stop-start).set_start(start+offset)
            clip.stroke_color = "black"
            clip.stroke_width = 25
            clip.stroke_color = None
            text.append(clip)
        a = CompositeVideoClip([self.video, CompositeVideoClip(text)])
        return VideoEditor(a)
    def composite_frame(self, duration, title):
        image = Image.open("frame.png")
        rat = image.height / image.width
        resized = np.array(image.resize((180, int(rat * 180))))
        frame = ImageClip(resized).set_start(0).set_duration(duration).set_pos(("center","center"))
        titleclip = TextClip(title, fontsize=10, font="SF-Compact-Rounded-Medium", color="white", size=(170, 80), method="caption").set_duration(duration).set_pos(("center","center"))
        return VideoEditor(CompositeVideoClip([self.video, frame, titleclip]))
    def save(self, name="file"):
        self.video.write_videofile(name + ".mp4")


def generate_text(subreddit=str,filter=PostFilter):
    getter = RedditGetter(
        'IPjLjyVHNlNu-98n8sEbIg',
        '8LjWFqgkXEgSu3jfXb6OmaB9Fweo4Q',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'
    ) 

    text = getter.get_posts(subreddit, 1, filter)

    content = text[0]['title'] + text[0]['selftext']
    content = content.replace("AITA", " am i the asshole ")
    content = content.replace("WIBTA", " would i be the asshole ")
    return content

def create(title, body):
    v = VideoFileClip("/Users/max/Desktop/VSCode/Python/RedditBot/gameplay.mp4")
    title_audio = AudioGetter().comp_audio(title)
    baudio = AudioGetter().comp_audio(body).set_start(title_audio.duration)
    final = CompositeAudioClip([baudio, title_audio])
    body_ = transcriber.generate(baudio)

    VideoEditor(v).resize().random_trim(final.duration).composite_frame(title_audio.duration, title).composite_audio(final).composite_text(body_, title_audio.duration).save()

getter = RedditGetter("Kjwa6iuQy8vAcVhF3KnIhA", "jS6cBOJv370uWfhLlu1fsiKTAHjLwQ", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0")

# post = getter.get_video_posts("BeAmazed", category=PostFilter.TOP, limit=1)
post = getter.get_posts("amitheasshole", category=PostFilter.TOP)

create(post[0].title, post[0].body[0:500])
