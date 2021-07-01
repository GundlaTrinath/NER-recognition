# importing require libraries
import speech_recognition as sr
from tkinter.filedialog import *
from moviepy.editor import *
from gtts import gTTS
import os
from PIL import ImageTk,Image
from pydub import AudioSegment
from pydub.silence import split_on_silence

# converting audio file to text
def get_large_audio_transcription(path='extracted.wav',r=sr.Recognizer()):
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

                Output = Label(root, text=text, bg='white', fg='#001a33')
                Output.pack(padx=30)
                print(chunk_filename,":",text)
                whole_text+=text



    return whole_text


# extracting audio from video
root=Tk()
root.title('Video to text Conversion')
root.configure(background='white')
root.iconbitmap(r'video_fiu_icon.ico')
root.geometry('1580x1000')


def video():
    wait = Label(root, text='Output will display here,please wait a moment', bg='white', fg='#001a33', font=('Arial', 10))
    wait.pack()
    video=askopenfilename()
    video=VideoFileClip(video)
    audio=video.audio
    audio.write_audiofile('extracted.wav')
    f1 = get_large_audio_transcription()



def audio():
    doc=gTTS(text=whole_text,lang='hi',slow=False)
    doc.save('Output_audio.wav')
    os.system('Output_audio.wav')

my_img=ImageTk.PhotoImage(Image.open("logo.png"))
my_label=Label(image=my_img,border=0).pack()
my_text=Label(root,text='Video to Audio Converter',bg="white",fg='#001a33',font=('Arial',20,'bold')).pack(pady=20)
label=Label(root,text='Upload a video',bg="white",fg='#001a33',font=('Arial',10,'bold')).pack()
photo=PhotoImage(file='icons8-browse-folder-80.png')
button=Button(root,image=photo,command=video,border=0,height=60,width=70).pack()
button=Button(root,padx=20,pady=15,bg='#001a33',fg='white',text='play audio file',command=audio).pack(pady=50)


root.mainloop()