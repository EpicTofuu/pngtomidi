import PIL.Image
import mido
from mido import MidiFile
from mido.midifiles.tracks import MidiTrack
import numpy
import tkinter.filedialog
import tkinter as tk
import math

root = tk.Tk()
frame = tk.Frame(root)
frame.grid()
    
UNIT = 10

def openImage():
    imgname = tkinter.filedialog.askopenfilename (title="select image", filetypes=(("png files","*.png"),("all files","*.*")))
    img = PIL.Image.open (imgname).convert ("L")
    
    data = numpy.array (img)

    
    mid = MidiFile (type = 1)
    maintrack = MidiTrack()
    #track = MidiTrack()
    #mid.tracks.append (track)
    
    for y in range (len(data)):
        row = data[y]
        rowdata = []

        rest = 0
        play = 0

        track = MidiTrack()

        for i in row:
            if i == 255:
                # rest
                rest += 1
                if play > 0:
                    rowdata.append (("p", play))
                    play = 0
            elif i == 0:
                play += 1
                if rest > 0:
                    rowdata.append (("r", rest))
                    rest = 0
        
        if play > 0:
            rowdata.append (("p", play))
            play = 0
            
        if rest > 0:
            rowdata.append (("r", rest))
            rest = 0

        for rd in rowdata:
            type, t = rd
            if type == "r":
                track.append (mido.Message ("note_off", note = 87 - y, velocity=127, time = t * UNIT))
            elif type == "p":
                track.append (mido.Message ("note_on", note = 87 - y, velocity=127, time = 0))  
                track.append (mido.Message ("note_off", note = 87 - y, velocity=127, time = t * UNIT))     
        
        mid.tracks.append (track)
        
    mid.save ("test.mid")
    print ("finished")


title = tk.Label (frame, text="png to midi")
title.grid(row=1,column=1)
author = tk.Label (frame,text="written by MaruMaru")
author.grid (row=2,column=1)

imagebtn=tk.Button(frame, text="choose image", command=openImage)
imagebtn.grid(row=3,column=0)

instbtn=tk.Button(frame, text="choose instruments")
instbtn.grid(row=3,column=1)

scalebtn=tk.Button(frame, text="choose scale (optional)")
scalebtn.grid(row=3,column=2)

root.mainloop()