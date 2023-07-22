import os
import ffmpeg

### Convert mpx (mp3 or mp4) into wav using ffmepg.
### 
### Need wav file for voice recognition with vosk
### Vosk
###     https://github.com/alphacep/vosk-api
###     install vosk
###         pip install vosk
### 
### install ffmpeg and ffmpeg-python
###     ffmpeg
###         download from https://github.com/BtbN/FFmpeg-Builds/releases
###         unzip and put files on an arbitrary directory
###         set path to the directory
###     ffmpeg-python
###         pip install ffmpeg-python
### 
### @param mpx  A string of mpx path
### @return     A string of mav path
def mpx2wav(mpx):
    print("-" * 60 + "\n")
    print("Converting mpx into wav" + "\n")
    print("-" * 60 + "\n")
    wav = mpx.removesuffix(".mp3").removesuffix(".mp4") + ".wav"
    # mpx to mpx
    if mpx.endswith("mp3"):
        tmp = mpx.removesuffix(".mp3") + "_tmp.mp3"
        stream = ffmpeg.input(mpx)
        stream = ffmpeg.output(stream, tmp, acodec="copy")
        ffmpeg.run(stream)
        # mpx to wav (to be continued)
        stream = ffmpeg.input(tmp)
    else:
        # mpx to wav (to be continued)
        stream = ffmpeg.input(mpx)
    # mpx to wav (continued)
    stream = ffmpeg.output(stream, wav, acodec="pcm_s16le", ac=1, ar=16000)
    ffmpeg.run(stream)
    # delete temporary file
    if mpx.endswith("mp3"):
        os.remove(tmp)
    return wav

# 
if __name__=="__main__":
    import tkinter.filedialog
    mpx = tkinter.filedialog.askopenfilename(filetypes=[("mp3,mp4", "*.mp*")])
    mpx2wav(mpx)
