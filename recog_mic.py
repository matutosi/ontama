import queue
import sys
import json
import sounddevice as sd
import datetime as dt
from vosk import Model, KaldiRecognizer

import voice_recog
import voice2docx

q = queue.Queue()

def convert(recog):
    voice_json = voice2docx.voice2json(recog)
    voice_dict = json.loads(voice_json)
    return voice_dict

def write_file(voice_dict, file = ""):
    if file == "":
        file = str(dt.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
    voice2docx.voice_dict2txt(voice_dict, file)
    docx = voice2docx.voice_dict2docx(voice_dict, file)

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

print("-" * 60 + "\n")
print("Preparing vosk (recognition tool)" + "\n")
print("-" * 60 + "\n")
recog = []

device = None
device_info = sd.query_devices(device, "input")
### soundfile expects an int, sounddevice provides a float:
samplerate = int(device_info["default_samplerate"])
model = Model("./vosk-model/model-ja")
log_res  = "ontama_log_res.txt"
log_text = "ontama_log_text.txt"

try:
    with(sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=device,
              dtype="int16", channels=1, callback=callback),
          open(log_res , "a", encoding = "utf-8") as f_res,
          open(log_text, "a", encoding = "utf-8") as f_text
        ):
        print("*" * 60 + "\n")
        print("Recognizing sound from microphone" + "\n")
        print("Press Ctrl+C to STOP" + "\n")
        print("*" * 60 + "\n")
        rec = KaldiRecognizer(model, samplerate)
        rec.SetWords(True) # record detail
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                res = rec.Result()
                text = voice_recog.extract_text(res)
                if text != "":
                    res = voice_recog.extract_result(res)
                    recog.append(res)
                    print(res, file = f_res) # log
                    print(text, file = f_text) # log
                    print(text + "\n")
                    print("-" * 60 + "\n")
                    print("Press Ctrl+C to STOP" + "\n")
                    print("-" * 60 + "\n")
except KeyboardInterrupt:
    stop_factor = "[Ctrl] + [c]"
    ### exit(0)
except Exception as e:
    stop_factor = str(e)
    ### exit(type(e).__name__ + ": " + str(e))
finally:
    print("*" * 60 + "\n")
    print("Stopped recognition with"  + stop_factor + "\n")
    print("*" * 60 + "\n")
    ### convert format
    voice_dict = convert(recog)
    ### write txt and docx
    write_file(voice_dict)
    exit(0)
