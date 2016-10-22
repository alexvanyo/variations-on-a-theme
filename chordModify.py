from music21 import *
import random

def writeGoodHarmony(fileName):
    melodyLine = converter.parse(fileName)
    harmonyLine = stream.Part()
    cMaj = scaleToNotes(scale.MajorScale('c#'), 'c#') #notes of a c major scale

    for currentNote in melodyLine.parts[0].notes:
        randChord = random.randint(0,2) - 1 #-1, 0, or 1
        harmonyName = cMaj[(cMaj.index(currentNote.name) + randChord*2)%8] #up a third, down a third, or same note
        harmonyNote = note.Note(harmonyName + '3') #makes it more'bass'
        harmonyLine.append(harmonyNote)

    melodyLine.append(harmonyLine)
    melodyLine.show()

def writeBadHarmony(fileName):
    melodyLine = converter.parse(fileName)
    harmonyLine = stream.Part()

    validIntervals = ['-m3', '-M3', '-P4', '-P8']  # possible chords

    for currentNote in melodyLine.parts[0].notes:
        randChord = random.randint(0, 3 )
        harmonyNote = currentNote.transpose(validIntervals[randChord]) #one of the 4 random intervals
        harmonyNote.octave = 3
        harmonyLine.append(harmonyNote)

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
print scaleToNotes(scale.MajorScale('c#'), 'c#')
