from music21 import *

nekedMelody = converter.parse('mary.mid')
melody = nekedMelody.makeMeasures()
melody.show('text')

def getMajorScale(tonic):
    """
    given the root/key, return pitchClasses of said key's major scale
    """
    scale = []
    for note in tonic.pitches:
        scale.append(note.pitchClass)
    return scale

def checkEnd(someObj):
    """
    given an object, check if it is the final Barline
    """
    return type(someObj) is bar.Barline and thisObj.style == final

def getDuration(thisNote):
    return thisNote.duration.quarterLength
def getKey():
    """
    simple key identifier, though assumes ALL notes are in the key, if key not
    already given
    """
    for measure in melody:
        for item in measure:
            if type(item) is key.Key:
                keySig = item
    if keySig is not None:
        return keySig

    numSharps = numFlats = 0
    uniqueAccs = set()
    for measure in melody:
        for item in measure:
            if type(item) is note.Note:
                thisPitch = item.pitch
                if thisPitch.accidental is not None:
                    if thisPitch not in uniqueAccs:
                        if thisPitch.accidental == flat:
                            numFlats += 1
                            uniqueAccs.add(thisPitch)
                        elif thisPitch.accidental == sharp:
                            numSharps += 1
                            uniqueAccs.add(thisPitch)
    keySig = key.Key(KeySignature(max(numSharps,numFlats)))
    return keySig

def createChords(scale):
    chords = stream.Part()
    for measure in melody:
        i = 0
        while i < len(measure):#for i in range(len(measure)):
            thisObj = measure[i]
            if type(thisObj) is note.Note:
                if thisObj.pitch.pitchClass in scale:
                    scaleDeg = scale.index(thisObj.pitch.pitchClass)
                    root = pitch.Pitch(scale[scaleDeg])
                    root.octave = 3
                    third = pitch.Pitch(scale[(scaleDeg+2)%7])
                    third.octave = 3
                    fifth = pitch.Pitch(scale[(scaleDeg+4)%7])
                    fifth.octave = 3
                    newChord = chord.Chord([root,third,fifth])
                    chordLen = getDuration(thisObj)

                    i += 1
                    while i < len(measure):#for i in range(len(measure)):
                        nextObj = measure[i]
                        if type(nextObj) is note.Note:
                            if abs(scale[scaleDeg] - nextObj.pitch.pitchClass) <= 2:
                                chordLen += getDuration(measure[i])
                                i += 1
                            else:
                                i -= 1
                                break
                        else:
                            i -= 1
                            break

                    newChord.duration = duration.Duration(chordLen)
                    chords.append(newChord)
            i+=1
    return chords

print getMajorScale(getKey())

nekedMelody.append(createChords(getMajorScale(getKey())))

nekedMelody.show()
