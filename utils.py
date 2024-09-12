import re
import math
import moviepy.editor
import moviepy.video
import requests

def count_syllables(word):
    word = replace_numbers_with_words(word)
    vowels = 'aeiouy'
    syllables = 0
    prev_char = None

    for char in word:
        char = char.lower()
        if char in vowels and (prev_char is None or prev_char not in vowels):
            syllables += 1
        prev_char = char

    if word.endswith('e'):
        syllables -= 1

    if syllables == 0:
        syllables = 1

    return syllables

def replace_numbers_with_words(text):
    pattern = re.compile(r'\d+')
    # result = pattern.sub(lambda x: num2words(int(x.group())), text)
    return "result"

def split_phrases(string, count=int):
    words = string.split()  # Split the string into individual words
    chunks = []
    current_chunk = []
    for i, word in enumerate(words):
        current_chunk.append(word)
        if i % 3 == 2:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
        elif i != len(words) - 1:
            current_chunk.append('\n')
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def break_text(text=str):
    c=0
    newtext=""
    for i in text:
        if i == " ":
            if c==2:
                newtext+="\n"
                c=0
                continue
            c+=1
        newtext+=i
    return newtext

def join_words(words, length):
    result = []
    for i in range(math.ceil(len(words) // length)):
        end = min((i + 1) * length, len(words))
        if i == len(words) // length: end = len(words)
        phrase = words[i * length: end]
        result.append(((phrase[0][0][0], phrase[-1][0][1]), " ".join([i[1] for i in phrase])))
    return result

class Post:
    def __init__(self, data: str) -> None:
        children = data[0]["data"]["children"][0]
        data = children['data']
        self.body = data["selftext"]
        self.title = data["title"]
        self.has_video = data["is_video"]
        self.video_url = None
        if self.has_video:
            self.video_url = data["secure_media"]["reddit_video"]["fallback_url"]
        
    def video(self, filename):
        if self.has_video:
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                try:
                    response = requests.get(self.video_url, stream=True)
                    response.raise_for_status()

                    for chunk in response.iter_content(chunk_size=8192):
                        temp_file.write(chunk)

                    temp_file_path = temp_file.name
                    from moviepy.editor import VideoFileClip
                    return VideoFileClip(filename=temp_file_path)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    return None

def save_temp(image):
    import tempfile
    from PIL import Image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        im = Image.fromarray(image)
        im.save(temp_file.name)
        return temp_file.name

def encode_image(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')