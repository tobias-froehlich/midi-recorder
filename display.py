import sys
import matplotlib.pyplot as plt
from utils import readEventsFromFile, transformEventsToNotes

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
    sys.exit()

filename = sys.argv[1]
print(filename)

events = readEventsFromFile(filename)

notes = transformEventsToNotes(events)  


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
    plt.fill_between([note["start_time"], note["end_time"]], [n-0.5, n-0.5], [n+0.5, n+0.5], color=channelColors[note["channel"]])
    

plt.show()

