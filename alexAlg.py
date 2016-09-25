import midi, random
file = midi.read_midifile("songs\\twinkle.mid")

# Get all note events
eventList = []
for event in file[0]:
    if type(event) is midi.NoteOnEvent:
        eventList.append(event)

# Combine an on/off node into a tuple
combinedList = []
for i in xrange(0, len(eventList), 2):
    combinedList.append((eventList[i].tick, eventList[i + 1].tick, eventList[i + 1].data[0]))

# Create the statistical list
statisticalList = {}
for i in xrange(0, len(combinedList) - 1):
    if statisticalList.has_key(combinedList[i]):
        if statisticalList[combinedList[i]].has_key(combinedList[i + 1]):
            statisticalList[combinedList[i]][combinedList[i + 1]] += 1
        else:
            statisticalList[combinedList[i]][combinedList[i + 1]] = 1
    else:
        statisticalList[combinedList[i]] = {combinedList[i + 1]: 1}

# Append the song with generate music of equal length
for i in xrange(0, len(eventList)):
    secondPreviousNote = file[0][-3]
    previousNote = file[0][-2]
    key = (secondPreviousNote.tick, previousNote.tick, previousNote.data[0])

    if statisticalList.has_key(key):
        choiceList = statisticalList[key]

        optionSum = 0
        for j in choiceList.values():
            optionSum += j

        selection = random.randint(1, optionSum)
        selectionSum = 0
        index = -1
        while selectionSum < selection:
            index += 1
            selectionSum += choiceList.values()[index]

        insertNote = choiceList.keys()[index]

    else:
        index = random.randint(0, len(statisticalList) - 1)
        insertNote = statisticalList.keys()[index]

    file[0].insert(-1, midi.NoteOnEvent(tick=insertNote[0], channel=0, data=[insertNote[2], 80]))
    file[0].insert(-1, midi.NoteOnEvent(tick=insertNote[1], channel=0, data=[insertNote[2], 0]))

print file

midi.write_midifile("songs\\output.mid", file)

