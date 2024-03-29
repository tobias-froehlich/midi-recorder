import mido
import datetime
import time
import threading
import os

midiInputPort = mido.open_input(
    name="recorder",
    client_name="recorder",
    virtual=True
)

midiOutputPort = mido.open_output(
    name="recorder",
    client_name="recorder",
    virtual=True
)

flag = [1,]
globals = {
    "file": None,
    "start": 0,
    "play_message": None,
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
        userInput = input("Enter \"file=...\", \"record\", \"play\", \"stop\", \"quit\":\n")
        if userInput == "quit":
            if globals["file"]:
                globals["file"].close()
            flag[0] = 0
        elif userInput.startswith("file="):
            newFilename = os.path.expanduser(userInput.split("=")[1])
            if os.path.exists(os.path.split(newFilename)[0]):
                filename = newFilename
            else:
                print("Directory does not exist.")
            print("file =", filename)
        elif userInput == "record":
            flag[0] = 2
            globals["start"] = time.time_ns()
            try:
                with open(filename, "r") as f:
                    for line in f:
                        pass
                last_time = int(line.strip().split(",")[0])
                globals["start"] = time.time_ns() - last_time - 10 * 1e9
                print("File exists. Append 10 seconds after end.")
            except FileNotFoundError:
                print("New file.")
            globals["file"] = open(filename, "a")
        elif userInput == "play":
            try:
                globals["file"] = open(filename, "r")
                globals["start"] = time.time_ns()
                flag[0] = 3
            except FileNotFoundError:
                print("File not found:", filename)
        elif userInput == "stop":
            if globals["file"]:
                globals["file"].close()
            stopAllNotes()
            flag[0] = 1
        


def listeningTask(flag, globals):
    while flag[0]:
        if flag[0] == 2:
            message = midiInputPort.poll()
            t = time.time_ns() - globals["start"]
            if message:
               event = "%i,%s,%i,%i,%i\n"%(t, message.type, message.channel, message.note, message.velocity)
               print(event)
               globals["file"].write(event)
               globals["file"].flush()
        if flag[0] == 3:
           if not globals["play_message"]:
               event = globals["file"].readline().strip().split(",")
               if len(event) == 5:
                   globals["play_message"] = mido.Message(
                       event[1],
                       channel=int(event[2]),
                       note=int(event[3]),
                       velocity=int(event[4])
                   )
                   t = int(event[0]) + globals["start"]
               else:
                   globals["file"].close()
                   globals["play_message"]
                   flag[0] = 1
                   print("Play end.")
           else:
               if time.time_ns() >= t:
                   print(globals["play_message"])
                   midiOutputPort.send(globals["play_message"])
                   globals["play_message"] = None
                   
                           
        time.sleep(0.001)

inputThread = threading.Thread(target=userInputTask, args=(flag, globals))
listeningThread = threading.Thread(target=listeningTask, args=(flag, globals))

inputThread.start()
listeningThread.start()

inputThread.join()
listeningThread.join()

midiInputPort.close()
