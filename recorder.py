import mido
import datetime
import time
import threading

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
    "file": None
}

filename = "/tmp/recording_" + datetime.datetime.now().isoformat() + ".txt"

def userInputTask(flag, globals):
    while flag[0]:
        userInput = input("Enter \"record\", \"stop\", \"quit\":\n")
        if userInput == "quit":
            if globals["file"]:
                globals["file"].close()
            flag[0] = 0
        elif userInput == "record":
            flag[0] = 2
            globals["file"] = open(filename, "a")
        elif userInput == "stop":
            if globals["file"]:
                globals["file"].close()
            flag[0] = 1
        


def listeningTask(flag, globals):
    while flag[0]:
        if flag[0] == 2:
            message = midiInputPort.poll()
            t = time.time_ns()
            if message:
               event = "%i,%s,%i,%i,%i\n"%(t,message.type, message.channel, message.note, message.velocity)
               print(event)
               globals["file"].write(event)
               globals["file"].flush()
           
                
        time.sleep(0.001)

inputThread = threading.Thread(target=userInputTask, args=(flag, globals))
listeningThread = threading.Thread(target=listeningTask, args=(flag, globals))

inputThread.start()
listeningThread.start()

inputThread.join()
listeningThread.join()

midiInputPort.close()
