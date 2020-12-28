# marumaru 2020

import PIL.Image
import midiutil as mu
import numpy
import tkinter.filedialog
import tkinter.messagebox
import tkinter.simpledialog
import tkinter as tk

root = tk.Tk()
frame = tk.Frame(root)
frame.grid()
    
UNIT = 10

DirName = "converted.mid"

Scales = [
    "None",
    "C major",
    "D major",
    "E major",
    "F major",
    "G major",
    "A major",
    "B major",
    "C minor",
    "D minor",
    "E minor",
    "F minor",
    "G minor",
    "A minor",
    "B minor",
]

scale = "None"

structures = {
    "major" : "TTSTTTS",
    "minor" : "TSTTSTS"     # using natural minor for now
}

oof = 69

Notes = {
    "C" : 0, 
    "D" : 2, 
    "E" : 4, 
    "F" : 5, 
    "G" : 7, 
    "A" : 9, 
    "B" : 11
    }

def openImage():
    print (scale)

    # imaging
    imgname = tkinter.filedialog.askopenfilename (title="select image", filetypes=(("png files","*.png"),("all files","*.*")))
    img = PIL.Image.open (imgname).convert ("P", palette=PIL.Image.ADAPTIVE, colors=2)
    img = img.convert ("L")
    img=img.resize ((172, img.width))
    #img.show()

    global data 
    data = numpy.array (img)

def start():# conversion
    if not "data" in globals():
        tkinter.messagebox.showinfo ("not image found", "no image was found\nplease use the choose image button in the menu to get started")
        return

    mid = mu.MIDIFile (1)
    
    for y in range (len(data)):
        row = data[y]
        rowdata = []

        note = 127-y

        key, structname = "", ""

        # account for scales
        if not scale == "None":
            key, structname = scale.split (" ")
            structure = structures[structname]

            cKey = note - (note % 12) + Notes[key]

            for n in structure:
                if n == "T":
                    cKey += 2
                elif n == "S":
                    cKey += 1

                if cKey + 1 == note:
                    note-=1
                elif cKey - 1 == note:
                    note+=1

        clength = 0
        cstart = 0

        for i in range(len(row)):
            item = row[i]

            if item == 0:
                if clength == 0:
                    cstart = i
                clength += 1
            elif item == 255:
                if clength > 0:
                    rowdata.append ((cstart,clength))
                    clength = 0
                
        if clength > 0:
            rowdata.append ((cstart,clength))
            clength = 0
                
        for rd in rowdata:
            st, le = rd
            mid.addNote (0, 0, note, st, le, 64)
                                        
    with open(DirName, "wb") as output_file:
        mid.writeFile(output_file)
        
    tkinter.messagebox.showinfo ("task completed", "the image has been converted")


def savefile ():
    global DirName
    DirName = tkinter.filedialog.asksaveasfilename (defaultextension='.mid', filetypes=[("midi files", '*.mid')], title="Choose filename")

def chooseScale ():
    root2 = tk.Tk()
    frame2 = tk.Frame(root2)
    frame2.pack()

    variable = tk.StringVar (frame2)
    variable.set (Scales[0])

    option = tk.OptionMenu (frame2, variable, *Scales)
    option.pack ()

    def ok():
        global scale
        scale = variable.get()
        root2.destroy()

    button = tk.Button(root2, text="OK", command=ok)
    button.pack()

title = tk.Label (frame, text="png to midi")
title.grid(row=1,column=1)
author = tk.Label (frame,text="written by MaruMaru, code available on github")
author.grid (row=2,column=1)

imagebtn=tk.Button(frame, text="choose image", command=openImage)
imagebtn.grid(row=3,column=0, sticky = tk.EW)

instbtn=tk.Button(frame, text="save as..", command=savefile)
instbtn.grid(row=3,column=1, sticky = tk.EW)

scalebtn=tk.Button(frame, text="choose scale (optional)", command=chooseScale)
scalebtn.grid(row=3,column=2, sticky = tk.EW)

startbtn=tk.Button(frame, text="start!", command=start)
startbtn.grid(row = 4, sticky = tk.EW, columnspan=3)

root.mainloop()