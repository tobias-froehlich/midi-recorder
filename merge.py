import os
import sys
from utils import readEventsFromFile, writeEventsToFile, \
        transformEventsToNotes, transformNotesToEvents

if len(sys.argv) != 2:
    print("Specify exactly one merge file!")
    sys.exit()

mergefilename = sys.argv[1]

print(mergefilename)

mergelines = []
try:
    with open(mergefilename, "r") as f:
        for line in f:
            mergelines.append(line)
except FileNotFoundError:
    print("The merge file was not found.")
    sys.exit()

for line in mergelines:
    words = line.strip().split()
    if len(words) == 0 or words[0] not in ["in", "out", "silence"]:
        print("Every line must start with \"in\" or \"out\" or \"silence\".")
        sys.exit()


outputfile = None
for line in mergelines:
    words = line.strip().split()
    if words[0] == "out":
        if outputfile == None:
            outputfile = os.path.join(os.path.split(mergefilename)[0], words[1])
        else:
            print("Specify only one output file in the merge file.")
            sys.exit()
        
if outputfile == None:
    print("Specify an output file in the merge file.")
    sys.exit()
        
print("Output file:", outputfile)

if not os.path.exists(os.path.split(outputfile)[0]):
    print("Output file path does not exist")
    sys.exit()


allNotes = []
offset = 0.0
for line in mergelines:
    words = line.strip().split()
    if words[0] == "in":
        filename = os.path.expanduser(words[1])
        starttime = float(words[2])
        print(starttime)
        endttime = float(words[3])
        events = readEventsFromFile(os.path.join(os.path.split(mergefilename)[0], filename))
        notes = transformEventsToNotes(events)
        newOffset = offset
        for note in notes:
            if note["end_time"] >= starttime \
                    and note["start_time"] <= endttime:
                allNotes.append({
                    "start_time": note["start_time"] + offset - starttime,
                    "end_time": note["end_time"] + offset - starttime,
                    "channel": note["channel"],
                    "note": note["note"],
                    "velocity": note["velocity"],
                })
            if note["end_time"] + offset - starttime > newOffset:
                newOffset = note["end_time"] + offset - starttime
        offset = newOffset
    if words[0] == "silence":
        offset += float(words[1])

allEvents = transformNotesToEvents(allNotes)
writeEventsToFile(allEvents, outputfile)
        


        
