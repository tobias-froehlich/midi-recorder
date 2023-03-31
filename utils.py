import sys

def readEventsFromFile(filename):
    events = []
    try:
        with open(filename, "r") as f:
            for line in f:
                words = line.strip().split(",")
                assert len(words) == 5
                events.append({
                    "time": int(words[0]),
                    "type": words[1],
                    "channel": int(words[2]),
                    "note": int(words[3]),
                    "velocity": int(words[4]),
                })
    except FileNotFoundError:
        print("File not found:", filename)
        sys.exit()
    return events

def writeEventsToFile(events, filename):
    with open(filename, "w") as f:
        for event in events:
            f.write("%i,%s,%i,%i,%i\n"%(
                int(event["time"]*1e9),
                event["type"],
                event["channel"],
                event["note"],
                event["velocity"],
            ))
    

def transformEventsToNotes(events):
    notes = []
    currentNotes = []
    for event in events:
        if event["type"] == "note_on" and event["velocity"] > 0:
            currentNotes.append({
                "start_time": event["time"],
                "channel": event["channel"],
                "note": event["note"],
                "velocity": event["velocity"],
            })
        elif event["type"] == "note_off" \
                or event["type"] == "note_on" and event["velocity"] == 0:
            for i in range(len(currentNotes)):
                note = currentNotes[i]
                if event["note"] == note["note"] \
                        and event["channel"] == note["channel"]:
                    completeNote = {
                        "start_time": note["start_time"] * 1e-9,
                        "end_time": event["time"] * 1e-9,
                        "channel": note["channel"],
                        "note": note["note"],
                        "velocity": note["velocity"],
                    }
                    notes.append(completeNote)
                    del currentNotes[i]
                    break
    return notes
            

def transformNotesToEvents(notes):
    events = []
    for note in notes:
        events.append({
            "time": note["start_time"],
            "type": "note_on",
            "channel": note["channel"],
            "note": note["note"],
            "velocity": note["velocity"],
        })
        events.append({
            "time": note["end_time"],
            "type": "note_off",
            "channel": note["channel"],
            "note": note["note"],
            "velocity": 0,
        })
    events.sort(key=lambda x: x["time"])
    return events
