from music21 import *
import random

halfDuration = duration.Duration(2)
quartDuration = duration.Duration(1)

s1 = stream.Stream()

def simpleFileRandomizer(file_name):
    songFile = converter.parse(file_name)
    pitches = []
    noteDurations = []
    for p in songFile.parts: #Gets list of all notes in midi file
        #print("Part: ", p.id)
        for n in p.flat.notes:#Tyep is <class 'music21.note.Note'>
            noteDurations.append(n.duration.type)
            pitches.append(n.nameWithOctave)
    print(noteDurations)
    print(pitches)
    uniquePitches = []
    for n in pitches: #Creates a list containing all of the unique notes in the midi
        if n not in uniquePitches:
            uniquePitches.append(n)
    print(uniquePitches)
    pitchFrequencies = []
    for pitch in uniquePitches: #Creates a 2D array that will contain corresponding frequencies of notes
        pitchFrequencies.append([])
    #print(pitchFrequencies)
    for i in range(len(pitches)-1): #Adds notes into the corresponding arrays, these notes will then be used to calculate the percent chance of the next note
        pitchIndex = uniquePitches.index(pitches[i])
        pitchFrequencies[pitchIndex].append(pitches[i+1])
    print(pitchFrequencies)
    noteSequence = []
    #NOTE: FOLLOWING SEQUENCE DOES NOT HAVE PENALIZING/REGENRATING PROBABILITIES IMPLEMENTED
    #DOES NOT ACCOUNT FOR CASES IN WHICH ONLY ONE OPTION IS AVAILABLE
    for i in range(len(pitches)):
        if i == 0:
            noteSequence.append(pitches[i])
        else: #All operations containing references to preceding note 2 are temporary in order to prevent constant repetition
            precedingNote2 = 0
            precNote2Pass = False
            try:
                precedingNote2 = noteSequence[i-2]
                precNote2Pass = True
            except:
                pass
            precedingNote = noteSequence[i-1]
            if precedingNote2 == precedingNote and precNote2Pass == True:
                nextNote = uniquePitches[random.randint(0,len(uniquePitches)-1)]
            else:
                nextNote = pitchFrequencies[uniquePitches.index(precedingNote)][random.randint(0,len(pitchFrequencies[uniquePitches.index(precedingNote)])-1)]
            noteSequence.append(nextNote)
    print(noteSequence)
    #http://web.mit.edu/music21/doc/moduleReference/modulePitch.html#music21.pitch.Pitch.midi
    #Guide for creating midi notes
    for i in range(len(noteSequence)):
        n = note.Note(noteSequence[i])
        if noteDurations[i] == 'quarter':
            n.duration = quartDuration
        elif noteDurations[i] == 'half':
            n.duration = halfDuration
        s1.append(n)
    s1.show('midi')


simpleFileRandomizer('MaryHadLittleLamb.mid')