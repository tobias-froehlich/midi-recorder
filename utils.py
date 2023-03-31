import sys

def readEventsFromFile(filename):
    events = []
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
    return events


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
            


