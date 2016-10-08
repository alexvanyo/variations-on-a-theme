from music21 import *
from algorithms import *
import os
import random

halfDuration = duration.Duration(2)
quartDuration = duration.Duration(1)

# Number of notes to check for penalties
PENALTY_HISTORY = 8

# Range between 0 and 1 for initial strictness for penalties:
# 1.0 - never repeat a note
# 0.5 - 50% of the normal probability for a note
# 0.0 - normal probability for a note
PENALTY_STRICTNESS = 0.8

# Amount that the penalty changes as the note gets further
# away from the current note:
# 0.1 - strictness decreases by 0.1 for every note
PENALTY_MODIFIER = 0.1

s1 = stream.Stream()

def get_notes(file_name):
    song_file = converter.parse(file_name)
    parts = {}
    for part in song_file.parts:
        pitches = []
        note_durations = []
        for thisNote in part.flat.notes:
            if type(thisNote) == chord.Chord:
                pitches.append(thisNote.pitchNames)
            elif type(thisNote) == note.Note:
                pitches.append(thisNote.nameWithOctave)
            elif type(thisNote) == note.Rest:
                pitches.append(thisNote.fullName)
            note_durations.append(thisNote.duration)
        parts[part] = pitches, note_durations
    return parts

def getThemes(file_name):
    parts = get_notes(file_name)

    for index, (part, (notes, note_durations)) in enumerate(parts.items()):
        print 'processing part {0} ...'.format(index)
        myStream = stream.Stream()
        theme = find_theme(zip(notes, note_durations))
        for noise in theme:
            if type(noise[0]) == list:
                thisNote = chord.Chord(noise[0])
            else:
                # print noise
                thisNote = note.Note(noise[0])
            thisNote.duration = noise[1]
            myStream.append(thisNote)
        if len(myStream.pitches) != 0:
            return myStream

def writeGoodHarmony(melStream):
    harmonyLine = stream.Part()
    cMaj = scaleToNotes(scale.MajorScale('c'), 'c') #notes of a c major scale

    for currentNote in melStream:
        randChord = random.randint(0,2) - 1 #-1, 0, or 1
        harmonyName = cMaj[(cMaj.index(currentNote.name) + randChord*2)%8] #up a third, down a third, or same note
        harmonyNote = note.Note(harmonyName + '3') #makes it more'bass'
        harmonyLine.append(harmonyNote)
    melodyLine = stream.Score()
    melodyLine.append(melStream)
    melodyLine.append(harmonyLine)
    melodyLine.show()

def scaleToNotes(changeScale, key):
    """
        gives you char array of notes in a scale
    """
    scaleNotes = []
    for currentPitch in changeScale.getPitches(key + '5', key + '6', direction='ascending'):
        scaleNotes.append(note.Note(currentPitch).name)

    return scaleNotes

def divideDictBy(dividingDict, divisor):
    dictCopy = dict(dividingDict)

    for key in dictCopy:
        dictCopy[key] /= float(divisor)

    return dictCopy

def simpleFileRandomizer(file_name):
    songFile = getThemes(file_name)
    pitches = []
    noteDurations = []
    for n in songFile: # Type is <class 'music21.note.Note'>
        noteDurations.append(n.duration.type)
        # assumes n is a single note
        pitches.append(n.nameWithOctave)
    # print(noteDurations)
    # print(pitches)
    uniquePitches = []
    for n in pitches: # Creates a list containing all of the unique notes in the midi
        if n not in uniquePitches:
            uniquePitches.append(n)
    # print(uniquePitches)

    # Pitch frequencies are recorded in a dictionary of dictionaries
    # Each note has a dictionary of all the notes that follow it mapped to the probability
    pitchFrequencies = {}
    for pitch in uniquePitches:
        pitchFrequencies[pitch] = {}

    # Adds notes into the corresponding dictionaries, just by count for looping
    for i in range(len(pitches)-1):
        pitchMap = pitchFrequencies[pitches[i]]

        pitchMap[pitches[i+1]] = pitchMap.get(pitches[i+1], 0) + 1

    # Generate default probabilities for each note/following note pair
    for pitch, pitchMap in pitchFrequencies.items():
        pitchFrequencies[pitch] = divideDictBy(pitchMap, sum(pitchMap.values()))

    noteSequence = []
    for i in range(len(pitches)):
        if i == 0:
            noteSequence.append(pitches[i])
        else:
            precedingNote = noteSequence[i-1]

            # Create a new probability map for the current state
            pitchMap = dict(pitchFrequencies[precedingNote])
            for noteName, probability in pitchMap.items():
                # Loop over past notes
                for j in xrange(0, PENALTY_HISTORY):
                    # Get the note to compare to
                    checkIndex = i - 1 - j

                    # Check for a valid index
                    if checkIndex < 0:
                        break

                    # Update the probabilities if we are repeating a note
                    if noteName == noteSequence[i - 1 - j]:
                        probabilityModifier = min(1, max(0, (1 - PENALTY_STRICTNESS) + j * PENALTY_MODIFIER))

                        pitchMap[noteName] *= probabilityModifier

            probabilitySum = sum(pitchMap.values())

            if probabilitySum == 0:
                # No valid note from the probabilities, just choose a random note
                nextNote = uniquePitches[random.randint(0, len(uniquePitches) - 1)]
            else:
                targetRandom = random.random()
                previousSum = 0

                # Weight the probabilities correctly
                tempProbList = divideDictBy(pitchMap, probabilitySum)

                # Get the next note from probabilities
                for noteName, probability in tempProbList.items():
                    previousSum += probability
                    if targetRandom < previousSum:
                        nextNote = noteName
                        break

            noteSequence.append(nextNote)
    # print(noteSequence)
    # http://web.mit.edu/music21/doc/moduleReference/modulePitch.html#music21.pitch.Pitch.midi
    # Guide for creating midi notes
    for i in range(len(noteSequence)):
        n = note.Note(noteSequence[i])
        if noteDurations[i] == 'quarter':
            n.duration = quartDuration
        elif noteDurations[i] == 'half':
            n.duration = halfDuration
        s1.append(n)

    writeGoodHarmony(s1)

simpleFileRandomizer('MaryHadLittleLamb.mid')
#simpleFileRandomizer('A_Farewell_to_a_Promised_Today.mid')
