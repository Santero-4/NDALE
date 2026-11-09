"""Handles the drag-and-drop and other widgets during the setup part"""
import json
import tkinter
import tkinter.ttk
import tkinter.filedialog
import glob
import pathlib
from PIL import Image, ImageTk
import display
import logic

path = ""
files = ""
niceNames = ""
config = {}
wd = ""
isPaused = False
global tick_id

def saveAll(filename):
    global wd
    with open(wd + filename +".json", "w+") as file:
        file.write(json.dumps(config, indent=2))

def getConfig():
    global config, wd
    file = tkinter.filedialog.askopenfile(initialdir = wd)
    loaded = json.load(file)
    if "C:" not in list(loaded.keys())[0]:
        if "graph"  in list(loaded.keys()):
            for key, value in loaded["graph"].items():
                config[wd+"/"+key] = [wd+"/"+v for v in value]
        else:
            for key, value in loaded.items():
                config[wd+"/"+key] = [wd+"/"+v for v in value]
    else:
        config = loaded


#Use native file picker to get folder of gifs
def getfiles(editor, fileslist, nnames):
    global path
    global files
    global niceNames
    global wd
    path = tkinter.filedialog.askdirectory(initialdir="./")
    if path:
        path = path + "/*.gif"
        filenames = glob.glob(path)
        print(path)
        if filenames:
            files = filenames
            niceNames = [pathlib.Path(file).stem for file in files]
            nnames.set(niceNames)
            fileslist.set(files)
            wd = str(pathlib.Path(files[0]).parent)
            editor.tkraise()


def matchSave(list, keys, vals, out):
    global config
    global files
    p = ""
    for key in keys:
        string = f"Saved {list[key]} -> "
        for v in vals:
            string = string + " " +list[v]
        config[files[key]] = [files[x] for x in vals]
        p = p + string + "\n"
    out.set(p)


def switch(window, cleanThis, activewindow = None):
    global config
    global wd, isPaused
    if cleanThis == "editor":
        with open(wd+"config.json", "w+") as file:
            file.write(json.dumps(config, indent=2))
    if cleanThis == "displaywindow":
        isPaused = True
        activewindow.canvas.photo = None


    window.tkraise()

def give_next():
    global config
    print("this happened")
    frames = []
    walk = logic.walk(config)
    for run in walk:
        frames.extend(display.open_and_resize(run))
    return frames


def tick(canvas, frames, i, n):
    global tick_id, isPaused
    frame = frames[i]
    img = frame[0]
    d = frame[1]
    canvas.photo = ImageTk.PhotoImage(img)
    canvas.itemconfig(canvas.item, image=canvas.photo)
    if i+1 == n:
        frames = give_next()
        n = len(frames)
        i = 0
    tick_id = canvas.after(d, tick, canvas, frames, (i+1), n)
    if isPaused:
        canvas.after_cancel(tick_id)


def play(canvas):
    global files, isPaused, config
    isPaused = False
    frames = []
    print(config.keys)
    walk = logic.walk(config)
    print(walk)
    for run in walk:
        frames.extend(display.open_and_resize(run))
    canvas.after(100, tick, canvas, frames, 0, len(frames))




def pause():
    global isPaused
    isPaused= True

#Read filenames and populate lists

#Let usr arrange graph  until they click play button in corner

#Save config and handoff to display



def main():
    #only run this once
    global files
    global niceNames
    root = tkinter.Tk()
    root.title("NDALE  V0")
    countrynames = ('Argentina', 'Australia', 'Belgium', 'Brazil',
                    'Canada', 'China', 'Denmark', 'Finland', 'France', 'Greece',
                    'India', 'Italy', 'Japan', 'Mexico', 'Netherlands', 'Norway',
                    'Spain', 'Sweden', 'Switzerland')
    cnames = tkinter.StringVar(value=countrynames)
    cnames = tkinter.StringVar(value=files)
    nnames = tkinter.StringVar(value="")

    splash = tkinter.ttk.Frame(root)
    splash.grid(column=0, row=0, sticky="nesw")
    editor = tkinter.ttk.Frame(root)

    tkinter.ttk.Button(splash, text="Open project", command= lambda: getfiles(editor, cnames, nnames)).grid(column=0, row=0)


    editor.grid(column=0, row = 0, sticky="nesw")
    single = tkinter.Listbox(editor, height=20,listvariable=nnames, selectmode="extended", exportselection=False)
    multi = tkinter.Listbox(editor, height=20,listvariable=nnames, selectmode="extended", exportselection=False)
    logText = tkinter.StringVar(value="No matchings saved yet")
    log = tkinter.Label(textvariable=logText)
    log.grid(row=2, column=0)
    tkinter.ttk.Button(editor, text="Save matching", command= lambda: matchSave(niceNames, single.curselection(), multi.curselection(), logText)).grid(row =2, column=1)
    multi.grid( row = 1, column=3)
    single.grid(row=1, column=1)

    filename = tkinter.StringVar()
    entry = tkinter.ttk.Entry(editor, textvariable=filename)
    entry.grid(row=3, column=3)
    tkinter.ttk.Button(editor, text="Save everything to disk. Filename:", command= lambda: saveAll(str(filename))).grid(row=3, column=2)
    tkinter.ttk.Button(editor, text = "Load from disk", command= getConfig).grid(row=3, column=1)

    displaywindow = tkinter.ttk.Frame(root)
    displaywindow.canvas = tkinter.Canvas(displaywindow, width= 512, height=512)
    displaywindow.canvas.grid(row=1, column=1)
    displaywindow.grid(column=0, row=0, sticky="nesw")
    tkinter.ttk.Button(displaywindow, text="Play", command= lambda: play(displaywindow.canvas)).grid(row=2, column=1)
    tkinter.ttk.Button(displaywindow, text="Pause", command=pause).grid(row=2, column=2)
    tkinter.ttk.Button(displaywindow, text="Export").grid(row=2, column=3)
    tkinter.ttk.Button(displaywindow, text="Edit", command= lambda: switch(editor, "displaywindow", displaywindow)).grid(row=2, column=4)
    displaywindow.canvas.item = displaywindow.canvas.create_image((256,256), anchor = "center")
    displaywindow.canvas.photo = None




    tkinter.ttk.Button(editor, text="View animation?", command= lambda: switch(displaywindow, "editor")).grid(row =2, column=2)



    splash.tkraise()

    root.mainloop()


if __name__ == "__main__":
    main()

