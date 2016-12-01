from music21 import *
from algorithms import *
import os, sys, argparse, atexit
import random
from collections import OrderedDict
from sys import argv

######## argument settings ########
f = None
piped_output = False
args = None

def no_verbose():
    global f, piped_output
    piped_output = True
    f = open(os.devnull, 'w')
    sys.stdout = f

def verbose():
    global piped_output
    if piped_output:
        f.close()
        sys.stdout = sys.__stdout__
    piped_output = False

def close_streams():
    verbose()

def start_up():
    no_verbose()

def set_args():
    global args
    parser = argparse.ArgumentParser(description='Variate some music.')
    parser.add_argument('-f', '--file', dest='file', help='input a file')
    parser.add_argument('-v', '--verbose', action='store_true', help='shows program output')
    parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    args = parser.parse_args()
    if args.verbose:
        verbose()
######## argument settings ########

FILE = '<midi file>'

halfDuration = duration.Duration(2)
quartDuration = duration.Duration(1)


# Number of notes to check for penalties
PENALTY_HISTORY = 8

# Range between 0 and 1 for initial strictness for penalties:
# 1.0 - never repeat a note
# 0.5 - 50% of the normal probability for a note
# 0.0 - normal probability for a note
PENALTY_STRICTNESS = 1.0

# Amount that the penalty changes as the note gets further
# away from the current note:
# 0.1 - strictness decreases by 0.1 for every note
PENALTY_MODIFIER = 0.1

# The multiplier on every note in the melody
THEME_WEIGHT = 1.5

def get_notes(file_name):
    song_file = converter.parse(file_name)
    parts = OrderedDict()
    for part in song_file.parts:
        pitches = []
        note_durations = []
        for thisNote in part.flat.notesAndRests:
            if type(thisNote) == chord.Chord:
                pitches.append(thisNote[0].nameWithOctave)
            elif type(thisNote) == note.Note:
                pitches.append(thisNote.nameWithOctave)
            elif type(thisNote) == note.Rest:
                pitches.append("rest")
            note_durations.append(thisNote.duration.quarterLength)
        parts[part] = pitches, note_durations
    return parts

def getThemes(file_name):
    parts = get_notes(file_name)

    for index, (part, (notes, note_durations)) in enumerate(parts.items()):
        print 'processing part {0} ...'.format(index)
        myStream = stream.Stream()
        theme = find_theme(zip(notes, note_durations))
        for noise in theme:
            if noise[0] == "rest":
                thisNote = note.Rest()
            elif type(noise[0]) == list:
                thisNote = chord.Chord(noise[0])
            else:
                # print noise
                thisNote = note.Note(noise[0])
            thisNote.duration = duration.Duration(noise[1])
            myStream.append(thisNote)
        if len(myStream.pitches) != 0:
            return myStream

def writeGoodHarmony(melStream):
    harmonyLine = stream.Part()
    cMaj = scaleToNotes(scale.MajorScale('c'), 'c') #notes of a c major scale

    for currentNote in melStream:
        if type(currentNote) == note.Rest:
            harmonyNote = note.Rest()

        else:
            randChord = random.randint(0,2) - 1 #-1, 0, or 1
            harmonyName = cMaj[(cMaj.index(currentNote.name) + randChord*2)%8] #up a third, down a third, or same note
            harmonyNote = note.Note(harmonyName + '3') #makes it more'bass'

        harmonyNote.duration = currentNote.duration
        harmonyLine.append(harmonyNote)

    melodyLine = stream.Score()
    melodyLine.append(melStream)
    melodyLine.append(harmonyLine)
    return melodyLine

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
    """ 
        main function 
    """

    s1 = stream.Score()

    songFile = get_notes(file_name)

    themes = getThemes(file_name)

    for part in songFile.values():
        part_stream = stream.Part()
        print part
        uniquePitches = []

        for n in part[0]: # Creates a list containing all of the unique notes in the midi
            if n not in uniquePitches:
                uniquePitches.append(n)
        # print(uniquePitches)

        # Pitch frequencies are recorded in a dictionary of dictionaries
        # Each note has a dictionary of all the notes that follow it mapped to the probability
        pitchFrequencies = {}
        for pitch in uniquePitches:
            print pitch
            pitchFrequencies[pitch] = {}

        # Adds notes into the corresponding dictionaries, just by count for looping
        for i in range(len(part[0])-1):
            pitchMap = pitchFrequencies[part[0][i]]

            pitchMap[part[0][i+1]] = pitchMap.get(part[0][i+1], 0) + 1

        # Generate default probabilities for each note/following note pair
        for pitch, pitchMap in pitchFrequencies.items():

            # Make the theme have a higher chance of being played
            for themeNote in themes:
                if themeNote.name != "rest":
                    for randomPitch, count in pitchMap.items():
                        if randomPitch == themeNote.nameWithOctave:
                            pitchMap[randomPitch] = pitchMap[themeNote.nameWithOctave] * THEME_WEIGHT
                            break

            pitchFrequencies[pitch] = divideDictBy(pitchMap, sum(pitchMap.values()))
        print pitchFrequencies

        noteSequence = []
        for i in xrange(len(part[0])):
            if part[0][i] == "rest":
                noteSequence.append("rest")
            elif i == 0:
                noteSequence.append(part[0][i])
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
            if noteSequence[i] == "rest":
                n = note.Rest()
            else:
                n = note.Note(str(noteSequence[i]))
            n.duration = duration.Duration(part[1][i])
            part_stream.append(n)

        s1.insert(0, part_stream)

    final_randomized_song = None
    # check number of parts
    if len(songFile) == 1:
        final_randomized_song = writeGoodHarmony(s1[0])
    else:
        final_randomized_song = s1
    print 'Task completed.'
    return final_randomized_song

def variate(file_name):
    print 'Attempting to variate \'{}\''.format(file_name)
    randomized_song = simpleFileRandomizer(file_name)
    return randomized_song


# only execute if running this directly
if __name__ == '__main__':
    atexit.register(close_streams)
    set_args()
    if not piped_output:
        no_verbose()
    if args.file:
        if os.path.exists(args.file):
            try:
                variate(args.file).show()
            except Exception as e:
                verbose()
                print e.message()
                print '(Hint: Are you sure the input file in valid format?)'
        else:
            verbose()
            print '\'{}\' is not a valid path.'.format(args.file)
    else:
        verbose()
        variate(FILE).show()

