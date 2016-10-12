from music21 import *
import random, numpy

halfDuration = duration.Duration(2)
quartDuration = duration.Duration(1)

s1 = stream.Stream()

def simpleFileRandomizer(file_name): #THERE IS NONFUNCTIONING CODE, THIS WILL NOT COMPILE
    songFile = converter.parse(file_name)
    pitches = []
    noteDurations = []
    for p in songFile.parts: # Gets list of all notes in midi file
        # print("Part: ", p.id)
        for n in p.flat.notes: # Type is <class 'music21.note.Note'>
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
    pitchFrequencies = []
    for pitch in uniquePitches: # Creates a 2D array that will contain corresponding frequencies of notes
        pitchFrequencies.append([])
    # print(pitchFrequencies)
    for i in range(len(pitches)-1): # Adds notes into the corresponding arrays, these notes will then be used to calculate the percent chance of the next note
        pitchIndex = uniquePitches.index(pitches[i])
        pitchFrequencies[pitchIndex].append(pitches[i+1])
    # print(pitchFrequencies)
    noteSequence = []
    # NOTE: FOLLOWING SEQUENCE DOES NOT HAVE PENALIZING/REGENRATING PROBABILITIES IMPLEMENTED
    # DOES NOT ACCOUNT FOR CASES IN WHICH ONLY ONE OPTION IS AVAILABLE
    for i in range(len(pitches)):
        if i == 0:
            noteSequence.append(pitches[i])
        else: # All operations containing references to preceding note 2 are temporary in order to prevent constant repetition
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
    # print(noteSequence)
    # http://web.mit.edu/music21/doc/moduleReference/modulePitch.html#music21.pitch.Pitch.midi
    # Guide for creating midi notes

    #CODE HERE IS NONFUNCTIONAL
    obtainedThemeInfo = getThemeInfo()
    for part in obtainedThemeInfo:
        for info in part:
            noteSequence[row][info[0]:info[0]+info[1]] = info[3] #This info[3] returns a themeID, may be matched to
                                                                    #a list of themes

    #All notes are created at this point, finally adding to stream
    for i in range(len(noteSequence)):
        n = note.Note(noteSequence[i])
        if noteDurations[i] == 'quarter':
            n.duration = quartDuration
        elif noteDurations[i] == 'half':
            n.duration = halfDuration
        s1.append(n)
    return (s1, pitches, noteSequence)

#simpleFileRandomizer('MaryHadLittleLamb.mid')

def getThemeInfo():
    """
    Does not currently work, ideally will return a 2D array of triples, with layer 1 of the array being the part
    and the values in those nested arrays be triples that are (indexLocation, length, themeID)
    """
    themeInfo = []

def getMelodyPart(file_name):
    pass

def getPartsInfo(file_name):
    songFile = converter.parse(file_name) #SummerNo3 has 14 instrument parts
    partsList = songFile.getElementsByClass(stream.Part) #Convenient list of parts
    noteList = []
    DurList = []
    OctList = []
    for i in range((len(partsList))): #Parses through the different parts
        noteList.append([])
        DurList.append([])
        OctList.append([])
        for m in range(len(partsList[i].getElementsByClass(stream.Measure))): #Iterates through measures
            for n in range(len(partsList[i].getElementsByClass(stream.Measure)[m].getElementsByClass(note.Note))): #Iterates through each note
                noteInList = partsList[i].getElementsByClass(stream.Measure)[m].getElementsByClass(note.Note)[n]
                noteList[i].append(noteInList) #Appends notes to list
                DurList[i].append(noteInList.duration.quarterLength)
                OctList[i].append(noteInList.octave)
    aDLSums = [] #Two one time arrays to just store the values of the sums
    aOLSums = []
    avgDurList = [] #For storing the average and determining the max
    avgOctList = []
    for i in range(len(DurList)):
        aDLSums.append(0)
        for val in DurList[i]:
            aDLSums[i] += val
    for i in range(len(OctList)):
        aOLSums.append(0)
        for val in OctList[i]:
            aOLSums[i] += val
    for i in range(len(DurList)):
        avgDurList.append(aDLSums[i]/len(DurList[i]))
    for i in range(len(OctList)):
        avgOctList.append(aOLSums[i]/len(OctList[i]))
    totalAverages = []
    for i in range(len(DurList)):
        totalAverages.append((avgDurList[i] + avgOctList[i])/2)

    return totalAverages.index(max(totalAverages)) #Returns max average index, this is also the index part number

def getPartsTest():
    songFile = corpus.parse('bach/bwv57.8')
    partsList = songFile.getElementsByClass(stream.Part) #Convenient list of parts
    noteList = []
    DurList = []
    OctList = []
    for i in range((len(partsList))): #Parses through the different parts
        noteList.append([])
        DurList.append([])
        OctList.append([])
        for m in range(len(partsList[i].getElementsByClass(stream.Measure))): #Iterates through measures
            for n in range(len(partsList[i].getElementsByClass(stream.Measure)[m].getElementsByClass(note.Note))): #Iterates through each note
                noteInList = partsList[i].getElementsByClass(stream.Measure)[m].getElementsByClass(note.Note)[n]
                noteList[i].append(noteInList) #Appends notes to list
                DurList[i].append(noteInList.duration.quarterLength)
                OctList[i].append(noteInList.octave)
    aDLSums = [] #Two one time arrays to just store the values of the sums
    aOLSums = []
    avgDurList = [] #For storing the average and determining the max
    avgOctList = []
    for i in range(len(DurList)):
        aDLSums.append(0)
        for val in DurList[i]:
            aDLSums[i] += val
    for i in range(len(OctList)):
        aOLSums.append(0)
        for val in OctList[i]:
            aOLSums[i] += val
    for i in range(len(DurList)):
        avgDurList.append(aDLSums[i]/len(DurList[i]))
    for i in range(len(OctList)):
        avgOctList.append(aOLSums[i]/len(OctList[i]))
    totalAverages = []
    for i in range(len(DurList)):
        totalAverages.append((avgDurList[i] + avgOctList[i])/2)

    print DurList
    print OctList
    print avgDurList
    print avgOctList
    print totalAverages

    print totalAverages.index(max(totalAverages))

getPartsTest()
#getPartsInfo('SummerNo3.mid')

def find_theme(notes):
    """
    David's algorithim for identifying the theme in a given list of notes
    """
    # print len(notes), notes
    def print_grid(grid):
        print numpy.matrix(grid)
    def get(r, c, grid):
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            return grid[r][c]
        else:
            return 0
    lookup_table = [[0 for j in xrange(len(notes))] for i in xrange(len(notes))]
    for row in xrange(len(lookup_table)):
        for column in xrange(len(lookup_table[row])):
            max_of_neighbors = max(
                get(row-1, column, lookup_table),
                get(row, column-1, lookup_table)
            )
            if row != column and notes[row] == notes[column]:
                lookup_table[row][column] = 1 + get(row-1, column-1, lookup_table)
            else:
                lookup_table[row][column] = max_of_neighbors
    theme_notes = []
    current = 0
    for index in xrange(len(notes)):
        if lookup_table[~0][index] > current:
            theme_notes.append(notes[index])
            current += 1
    # print_grid(lookup_table)
    return theme_notes