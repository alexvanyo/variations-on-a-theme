from music21 import *

nekedMelody = converter.parse('mary.mid')
melody = nekedMelody.makeMeasures()
melody.show('text')

def getMajorScale(tonic):
    scale = []
    for note in tonic.pitches:
        scale.append(note.pitchClass)
    return scale

def getDuration(thisNote):
    print thisNote.duration.quarterLength
    return thisNote.duration.quarterLength#duration.convertTypeToNumber(thisNote.duration.type)
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
        for i in range(len(measure)):
            if type(measure[i]) is note.Note:
                if measure[i].pitch.pitchClass in scale:
                    scaleDeg = scale.index(measure[i].pitch.pitchClass)
                    root = pitch.Pitch(scale[scaleDeg])
                    root.octave = 3
                    third = pitch.Pitch(scale[(scaleDeg+2)%7])
                    third.octave = 3
                    fifth = pitch.Pitch(scale[(scaleDeg+4)%7])
                    fifth.octave = 3
                    newChord = chord.Chord([root,third,fifth])
                    chordLen = getDuration(measure[i])#measure[i].duration
                    """
                    i += 1
                    for i in range(len(measure)):
                        if type(measure[i]) is note.Note:
                            #print abs(scale[scaleDeg] - measure[i].pitch.pitchClass)
                            if abs(scale[scaleDeg] - measure[i].pitch.pitchClass) <= 2:
                                chordLen += getDuration(measure[i])
                                #print chordLen
                                i += 1
                            else:
                                i -= 1
                                print 'broken af'
                                break
                    print chordLen, newChord
                    """
                    newChord.duration = duration.Duration(chordLen)
                    chords.append(newChord)

    return chords

print getMajorScale(getKey())

nekedMelody.append(createChords(getMajorScale(getKey())))

nekedMelody.show()
