# importing require libraries
import speech_recognition as sr
from tkinter.filedialog import *
from moviepy.editor import *
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence


# extracting audio from video
video=askopenfilename()
video=VideoFileClip(video)
audio=video.audio
audio.write_audiofile('extracted.wav')
print('extracted audio file')


# converting audio file to text
r=sr.Recognizer()
def get_large_audio_transcription(path):
    sound=AudioSegment.from_wav(path)
    chunks=split_on_silence(sound,min_silence_len=500,silence_thresh=sound.dBFS-14,keep_silence=500)
    folder_name='audio_chunks'
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    global whole_text
    whole_text=""
    print("processing...")
    for i,audio_chunk in enumerate(chunks,start=1):
        chunk_filename=os.path.join(folder_name,f"chunk{i}.wav")
        audio_chunk.export(chunk_filename,format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listed=r.listen(source)
            try:
                text=r.recognize_google(audio_listed,language="hi-IN")
            except sr.UnknownValueError as e:
                print('error:',str(e))
            else:
                text=f"{text.capitalize()}. "
                print(chunk_filename,":",text)
                whole_text+=text
    return whole_text

path='extracted.wav'
print('\nFull text:',get_large_audio_transcription(path))

doc=gTTS(text=whole_text,lang='hi',slow=False)
doc.save('hindi.wav')
os.system("hindi.wav")