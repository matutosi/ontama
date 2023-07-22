import time
import tkinter as tk

def set_buttons():
    global root
    root = tk.Tk()
    root.title('ONTAMA (ONsei Totally Analyze system by MAtsumura)')
    root.geometry('400x100')
    title = tk.Label(root, text =" Recognize from", font = ("", "16"), anchor = tk.E)
    b_file = tk.Button(root, text = 'File (wav, mp3, mp4)', font = ("", 12), command = from_file)
    b_mic  = tk.Button(root, text = 'Microphone'          , font = ("", 12), command = from_mic)
    title.pack()
    b_file.pack()
    b_mic.pack()
    # b_sys  = tk.Button(root, text = 'System sound'        , font = ("", 12), command = from_sys)
    # b_sys.pack()
    root.mainloop()

def from_file():
    root.destroy()
    import recog_file

def from_mic():
    root.destroy()
    import recog_mic

# def from_sys():
#     import recog_sys

set_buttons()
