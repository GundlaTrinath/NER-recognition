# importing require libraries
import speech_recognition as sr
from tkinter.filedialog import *
from moviepy.editor import *
from gtts import gTTS
import os
from PIL import ImageTk,Image
from pydub import AudioSegment
from pydub.silence import split_on_silence
import nltk
import pandas as pd
from spacy import displacy
import spacy
# -------------------------------------------------------------converting hindi audio file to text---------------------------------------------------------------------------

def get_large_audio_transcription_hin(path='extracted.wav',r=sr.Recognizer()):
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
    wait1.config(text='Extracted Completed')

    return whole_text


# -------------------------------------------------------------converting english audio file to text---------------------------------------------------------------------------

def get_large_audio_transcription_eng(path='extracted.wav',r=sr.Recognizer()):
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
                text=r.recognize_google(audio_listed)
            except sr.UnknownValueError as e:
                print('error:',str(e))
            else:
                text=f"{text.capitalize()}. "
                print(chunk_filename,":",text)
                whole_text+=text
    wait2.config(text='Extracted Completed')

    return whole_text

def text2():
    text2=open('output(english).txt','w+')
    text2.write(whole_text)
    text2.close()

def text1():
    f2 = open("output(hindi).txt",'w+',encoding="utf-8")
    f2.write(whole_text)
    f2.close()

def ner_extract():
    global wait1
    waitn = Label(root, text='Entity file generated', bg='white', fg='black', font=('Arial', 13,'bold'))
    waitn.pack()
    content = whole_text
    print("loading model..")
    model = spacy.load("en_core_web_trf")
    print("model loaded")
    doc = model(content)
    entities = []
    labels = []
    start_pos = []
    end_pos = []
    for ent in doc.ents:
        entities.append(ent)
        labels.append(ent.label_)
        start_pos.append(ent.start_char)
        end_pos.append(ent.end_char)
    df = pd.DataFrame({'Entities':entities,
                   'Labels':labels,
                   'Position_Start':start_pos,
                   'Position_end':end_pos})
    df.to_csv("Entities.csv")
    

root=Tk()
root.title('NER from Video&Audio')
root.iconbitmap(r'video_fiu_icon.ico')
root.geometry('1500x700')


# ---------extracting audio from video---------
def video1():
    global wait1
    wait1 = Label(root, text='Please wait a moment', bg='white', fg='black', font=('Arial', 13,'bold'))
    wait1.pack()
    video=askopenfilename()
    video=VideoFileClip(video)
    audio=video.audio
    audio.write_audiofile('extracted.wav')
    f1 = get_large_audio_transcription_hin()

# ---------extracting audio from video---------
def video2():
    global wait2
    wait2 = Label(text='Please wait a moment', bg='white', fg='black', font=('Arial', 13,'bold'))
    wait2.pack()
    video=askopenfilename()
    video=VideoFileClip(video)
    audio=video.audio
    audio.write_audiofile('extracted.wav')
    f1 = get_large_audio_transcription_eng()


# ----------audio Output (hindi)-------------
def audio1():
    doc=gTTS(text=whole_text,lang='hi',slow=False)
    doc.save('Output_audio_hin.wav')


# ----------audio Output (english)-------------
def audio2():
    doc=gTTS(text=whole_text,lang='en',slow=False)
    doc.save('Output_audio_eng.wav')

newsize = (1500, 700)
im = Image.open(r"bgcol.png")
im = im.resize((newsize), Image.ANTIALIAS)
my_bg=ImageTk.PhotoImage(im)
my_bglabel=Label(image=my_bg).place(x=-5,y=0)
my_img=ImageTk.PhotoImage(Image.open("bglabel.png"))
my_label=Label(image=my_img,border=0).pack(pady=100)
my_text1=Label(root,text='Select video (HINDI)',font=('Arial',13,'bold')).place(x=900,y=250)
#label.config(bg='gray')
#root.wm_attributes('', root['bg'])
my_text2=Label(root,text='Select video (ENGLISH)',font=('Arial',13,'bold')).place(x=285,y=250)
label = Label(root, text='Upload a Video', bg='white', fg='black', font=('Arial', 13,'bold')).pack()
button1=Button(root,width=20,height=2,bg='#df514a',fg='white',border=2,text='Browse',font=('Arial',10,'bold'),command=video1).place(x=900,y=300)
button2=Button(root,width=20,height=2,bg='#df514a',fg='white',border=2,text='Browse',font=('Arial',10,'bold'),command=video2).place(x=300,y=300)
button3=Button(root,width=20,height=2,bg='#df514a',fg='white',border=2,text='Download Audio file ↓\n(Hindi)',font=('Arial',15,'bold'),command=audio1).place(x=20,y=500)
button4=Button(root,width=20,height=2,bg='#df514a',fg='white',border=2,text='Download Audio file ↓\n(English)',font=('Arial',15,'bold'),command=audio2).place(x=350,y=500)
button5=Button(root,width=20,height=2,bg='#df514a',fg='white',border=2,text='Download Text file ↓\n(Hindi)',font=('Arial',15,'bold'),command=text1).place(x=750,y=500)
button6=Button(root,width=20,height=2,bg='#df514a',fg='white',border=2,text='Download Text file ↓\n(English)',font=('Arial',15,'bold'),command=text2).place(x=1100,y=500)
#my_text3=Label(root,text='STEPS TO FOLLOW :-',bg="white",fg='black',font=('Arial',15,'bold')).place(x=10,y=630)
#button7=Button(root,width=20,height=2,bg='#df514a',fg='white',border=2,text='Browse',font=('Arial',10,'bold'),command=).place(x=600,y=300)
button7=Button(root,width=20,height=2,bg='#df514a',fg='white',border=2,text='Download MetaData',font=('Arial',15,'bold'),command=ner_extract).place(x=570,y=590)

root.mainloop()