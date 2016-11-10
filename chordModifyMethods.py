from music21 import *

COMMON_PROGRESSIONS = [4,5,1,-4,-5,-1]

nekedMelody = converter.parse('mary.mid')
melody = nekedMelody.makeMeasures()

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
    """
    given a note of class note.Note, return its length in quarter notes
    """
    return thisNote.duration.quarterLength

def getKey(melody):
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

def getChordStructure(chordScale):
    chordStruct = []
    for note in chordScale:
        scaleDeg = chordScale.index(note)
        root = pitch.Pitch(chordScale[scaleDeg])
        root.octave = 3
        third = pitch.Pitch(chordScale[(scaleDeg+2)%7])
        third.octave = 3
        fifth = pitch.Pitch(chordScale[(scaleDeg+4)%7])
        fifth.octave = 3
        newChord = chord.Chord([root,third,fifth])

        chordStruct.append(newChord)

    return chordStruct

def getNextChord(chordStruct, root):
    for thisChord in chordStruct:
        if thisChord.fifth.pitchClass == root.pitch.pitchClass:
            return chord.Chord(thisChord.pitches)

    return None

def checkChordProgression(chordStruct, currChords, lastChord, currNote):
    chordNum = 0
    compareChord = currChords[lastChord]
    for i in range(len(chordStruct)):
        if chordStruct[i].root().pitchClass == compareChord.root().pitchClass:
            chordNum = i

    for interval in COMMON_PROGRESSIONS:
        if currNote in chordStruct[(chordNum + interval)%7]:
            return chordStruct[(chordNum + interval)%7]
    return None

def checkStartChord(chordStruct, checkNote):
    print checkNote, chordStruct[0]
    for interval in chordStruct[0].pitches:
        if checkNote.pitchClass == interval.pitchClass:
            return chordStruct[0]
    return None

def createChords(scale):
    chordStruct = getChordStructure(scale)
    chords = stream.Part()
    isStart = True
    currChord = -1 #used to keep track of the last chord index, for sake of chord progression

    for measure in melody:
        i = 0
        while i < len(measure):
            thisObj = measure[i]
            if type(thisObj) is note.Note:
                if thisObj.pitch.pitchClass in scale:
                    if isStart == True:
                        newChord = checkStartChord(chordStruct, thisObj)
                        isStart = False
                    else:
                        newChord = checkChordProgression(chordStruct, chords, currChord, thisObj)
                    if newChord is None:
                        newChord = getNextChord(chordStruct, thisObj)

                    chordLen = getDuration(thisObj)

                    i += 1
                    while i < len(measure):
                        nextObj = measure[i]
                        if type(nextObj) is note.Note:
                            if abs(thisObj.pitch.pitchClass - nextObj.pitch.pitchClass) <= 2:
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
                    currChord += 1
            i+=1
    return chords

nekedMelody.append(createChords(getMajorScale(getKey(melody))))

nekedMelody.show()
