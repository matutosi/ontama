from vosk import Model, KaldiRecognizer, SetLogLevel
import tkinter.filedialog
import wave
import json
from docx import Document

import voice_recog
import voice2docx
import mpx2wav

filetypes = [("wav,mp3,mp4", ".wav .mp3 .mp4")]
file = tkinter.filedialog.askopenfilename(filetypes = filetypes)
if file.endswith("wav"):
    wav = file
else: 
    wav = mpx2wav.mpx2wav(file)

### recognize voice
recog = voice_recog.voice_recog(wav)
### txt = write_recog(recog, wav)

### convert format
voice_json = voice2docx.voice2json(recog)
voice_dict = json.loads(voice_json)

### write txt
voice2docx.voice_dict2txt(voice_dict, wav)
### write docx
docx = voice2docx.voice_dict2docx(voice_dict, wav)
