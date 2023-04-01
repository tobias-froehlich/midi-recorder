import mido
import datetime
import time
import threading
import os
from utils import readEventsFromFile

midiOutputPort = mido.open_output(
    name="recorder",
    client_name="recorder",
    virtual=True
)

flag = [1,]
globals = {
    "startClock": 0,
    "startTime": 0,
    "events": [],
    "event": None,
    "index": 0,
}


def stopAllNotes():
    for channel in range(16):
        for note in range(128):
            midiOutputPort.send(mido.Message(
                "note_off",
                channel=channel,
                note=note
            ))

def userInputTask(flag, globals):
    filename = "/tmp/recording_" + datetime.datetime.now().isoformat() + ".txt"
    while flag[0]:
        userInput = input("Enter \"file=...\", \"play\", \"stop\", \"quit\":\n")
        if userInput == "quit":
            flag[0] = 0
        elif userInput.startswith("file="):
            newFilename = os.path.expanduser(userInput.split("=")[1])
            if os.path.exists(os.path.split(newFilename)[0]):
                filename = newFilename
            else:
                print("Directory does not exist.")
            print("file =", filename)
            
        elif userInput.startswith("play"):
            words = userInput.strip().split()
            if words[0] == "play":
                globals["events"] = readEventsFromFile(filename)
                if len(words) == 2:
                    globals["startTime"] = int(float(words[1]) * 1e9)
                else:
                    globals["startTime"] = 0
            globals["index"] = 0
            t = globals["events"][0]["time"]
            while t < globals["startTime"] and globals["index"] < len(globals["events"]) - 1:
                globals["index"] += 1
                t = globals["events"][globals["index"]]["time"]                
            print(globals["index"])
            globals["startClock"] = time.time_ns()
            flag[0] = 3
        elif userInput == "stop":
            stopAllNotes()
            flag[0] = 1
        


def listeningTask(flag, globals):
    while flag[0]:
        if flag[0] == 3:
           event = globals["events"][globals["index"]]
           if time.time_ns() >= globals["startClock"] + event["time"] - globals["startTime"]:
                print(event)
                midiOutputPort.send(mido.Message(
                    event["type"],
                    channel=event["channel"],
                    note=event["note"],
                    velocity=event["velocity"],
                ))
                globals["index"] += 1
                if globals["index"] >= len(globals["events"]):
                    print("Play end.")
                    flag[0] = 1
                                                           
        time.sleep(0.001)

inputThread = threading.Thread(target=userInputTask, args=(flag, globals))
listeningThread = threading.Thread(target=listeningTask, args=(flag, globals))

inputThread.start()
listeningThread.start()

inputThread.join()
listeningThread.join()

midiOutputPort.close()
