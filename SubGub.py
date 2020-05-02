import os
import hashlib
import sys
import requests
import time
import tkinter as tk
from tkinter import filedialog
from pyfiglet import Figlet


def getBanner():
    f = Figlet(font='graffiti')
    print(f.renderText('Subtitle Grabber'))

def selectMovie():
    print("Select the Movie on prompt\n")
    time.sleep(2)
    fileName_ = filedialog.askopenfilename(initialdir="/",title="Open File",filetypes=(("Text Files","*.txt"),("All Files","*.*")))
    if fileName_ == "":
        print("No Movie was selected.....Exiting")
        exit()
    else:
        filterMovieName_ = fileName_.split("/")
        print("Movie selected is : {0}\n".format(filterMovieName_[-1]))
        return fileName_

def getSubtitle(movieName):
    getMovieDetails_ = movieName.rpartition(".")
    temp = list(getMovieDetails_)
    temp[-1] = "srt"
    # Path will always get divided into three parts (1. Path till Slash "/" 2. delimeter 3. extension)
    # Can be optimised
    absolutePath_ = temp[0]+temp[1]+temp[2]
    

    headers = {"User-Agent":"SubDB/1.0 (Sahil/1.0; http://github.com/koortix)"}
    movieHash = get_hash(movieName)
    #print("Hash is : {0}".format(movieHash))
    req_ = requests.get(f'http://api.thesubdb.com/?action=search&hash={movieHash}',headers=headers) 
    
    getLanguages_ = req_.text.split(',')
    for language in getLanguages_:
        print("Available Languages for this movie are : {0}".format(language))


    getUserInput_ = input("Enter the language code for download : ")

    getSubReq_ = requests.get(f'http://api.thesubdb.com/?action=download&hash={movieHash}&language={getUserInput_}',headers=headers) 
    #print(getSubReq_.headers)
    getAttachment_ = getSubReq_.headers.get('Content-Disposition').split("=")
    
    try:
        with open(absolutePath_,'wb') as f:
            f.write(getSubReq_.content)
        print("\nSubtitle is Downloaded at {0}".format(absolutePath_))
    except Exception:
        print(Exception)
    except KeyboardInterrupt:
        print("Keyboard Interrupt by user")

def get_hash(name):
    try:
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            size = os.path.getsize(name)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
            return hashlib.md5(data).hexdigest()
    except Exception:
        print("Invalid File...Select the correct movie file")
        exit()

def checkPyVersion():
    if sys.version_info[0] < 3:
        print("This script need Python 3 or higher")
    exit()

if __name__ == "__main__":
    getBanner()
    root = tk.Tk()
    root.withdraw()
    finalMovieName_ = selectMovie()
    getSubtitle(finalMovieName_)