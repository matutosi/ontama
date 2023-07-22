from vosk import Model, KaldiRecognizer, SetLogLevel
import wave
import tkinter.filedialog
import json

### Voice recognition with vosk.
### 
### @param wav A string of wav path
### @return A list including strings of voice recognition with vosk.
def voice_recog(wav):
    print("-" * 60 + "\n")
    print("Preparing vosk (recognition tool)" + "\n")
    print("-" * 60 + "\n")
    SetLogLevel(0)
    # read wav file
    wf = wave.open(wav, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)
    # set model
    model = Model("./vosk-model/model-ja")
    # set recognition
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    recog = []
    # voice recognition
    print("-" * 60 + "\n")
    print("Recognizing voice" + "\n")
    print("-" * 60 + "\n")
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = rec.Result()
            recog.append(extract_result(res))
            print(extract_text(res))
    # final result
    res = rec.FinalResult()
    recog.append(extract_result(res))
    print(extract_text(res))
    return recog

### Extract result filed from a result of voice recognition with vosk.
### 
### @param res  A result of voice recognition with vosk.
### @return     A string.
def extract_result(res):
    res_json = json.loads(res)
    res_str = "{}".format(res_json.get("result"))
    return res_str

### Extract text filed from a result of voice recognition with vosk.
### 
### @param res  A result of voice recognition with vosk.
### @return     A string.
def extract_text(res):
    res_json = json.loads(res)
    text = "{}".format(res_json.get("text"))
    return text

### Write voice recognition result with vosk into a text file.
### 
### @param recog  A list including strings of voice recognition with vosk
### @param wav    A string of wav path
### @return  A string of text path
def write_recog(recog, wav):
    txt = wav.removesuffix(".wav") + ".txt"
    with open(txt, mode = "w", encoding = "utf-8") as f:
        f.write("\n".join(recog))
    return txt

# 
if __name__=="__main__":
    wav = tkinter.filedialog.askopenfilename(filetypes=[("wav", "*.wav")])
    recog = voice_recog(wav)
    write_recog(recog, wav)
