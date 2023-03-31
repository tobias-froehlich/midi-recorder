import sys
import matplotlib.pyplot as plt

channelColors = [
    "red",
    "saddlebrown",
    "darkorange",
    "gold",
    "darkgoldenrod",
    "olivedrab",
    "limegreen",
    "mediumaquamarine",
    "darkcyan",
    "dodgerblue",
    "royalblue",
    "darkblue",
    "blue",
    "blueviolet",
    "mediumvioletred",
    "hotpink",
]




if len(sys.argv) != 2:
    print("Specify exactly one file!")

filename = sys.argv[1]
print(filename)

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

notes = []
currentNotes = []
for event in events:
    if event["type"] == "note_on":
        currentNotes.append({
            "start_time": event["time"],
            "channel": event["channel"],
            "note": event["note"],
            "velocity": event["velocity"],
        })
    elif event["type"] == "note_off":
        for i in range(len(currentNotes)):
            note = currentNotes[i]
            if event["note"] == note["note"] \
                    and event["channel"] == note["channel"]:
                print("bla", note["start_time"] * 1e-9)
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
            

endtime = events[-1]["time"] * 1e-9
print(endtime)

for i in range(128):
    if i == 60:
        color = 'white'
    elif i % 12 in [1, 3, 6, 8, 10]:
        color = 'darkgray'
    else:
        color = 'lightgray'

    plt.fill_between([0, endtime], [i-0.5, i-0.5], [i+0.5, i+0.5], color=color)
    plt.plot([0, endtime], [i-0.5, i-0.5], color="white")


#for i in range(16):
#    print(channelColors[i])
#    plt.fill_between([2, 3], [5*i-0.5, 5*i-0.5], [5*i+0.5, 5*i+0.5], color=channelColors[i])

for note in notes:
    n = note["note"]
    plt.fill_between([note["start_time"], note["end_time"]], [n-0.5, n-0.5], [n+0.5, n+0.5], color=channelColors[note["channel"] - 1])
    

plt.show()

