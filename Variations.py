import midi

pattern = midi.read_midifile("Mary had a little lamb.mid")

# groups notes in a MIDI file into pairs
def groupNotes(pattern):
    rawNotes = [] # default notes
    notes = [] # grouped notes
    note = 0
    newNote = 0

    # adds all notes with a positive duration to rawNotes
    for i in xrange(len(pattern[0])):
        if (isinstance(pattern[0][i], midi.NoteOnEvent)):
            if (pattern[0][i].data[1] != 0):
                rawNotes.append(pattern[0][i].data[0])

    # initializes the 2D array notes
    for i in xrange(len(rawNotes)/2):
        temp = []
        for j in xrange(2):
            temp.append(0)
        notes.append(temp)

    # adds the rawNotes to notes in pairs, if rawNotes is odd it adds the last note with a pair of -1
    j = 0
    last = 0
    for i in range(len(rawNotes)-1):
        if (j+1 <= len(rawNotes)-1):
            notes[i] = [rawNotes[j],rawNotes[j+1]]
            last = notes[i][1]
        else:
            notes.append([rawNotes[len(rawNotes)-1],-1])
            break
        j += 2

    # returns the grouped notes
    return notes

notes = groupNotes(pattern)
# prints for aesthetics
for i in xrange(len(notes)):
    print notes[i]