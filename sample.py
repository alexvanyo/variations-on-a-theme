import music21 as music
from algorithms import *
from AndyTestFileVariations import getPartsInfo
import os

SONG = 'fur_elise'
FOLDER = 'songs'
DIRECTORY = '{0}/{1}'.format(FOLDER, SONG)
FILE = '{0}.mid'.format(DIRECTORY)

# if not os.path.exists(DIRECTORY):
    # print 'made', DIRECTORY
    # os.makedirs(DIRECTORY)


def get_notes(file_name):
    try:
        song_file = music.converter.parse(file_name)
        parts = {}
        for part in song_file.parts:
            pitches = []
            note_durations = []
            for note in part.flat.notes:
                print note.xPosition
                if type(note) == music.chord.Chord:
                    pitches.append(note.pitchNames)
                elif type(note) == music.note.Note:
                    pitches.append(note.nameWithOctave)
                elif type(note) == music.note.Rest:
                    pitches.append(note.fullName)
                note_durations.append(note.duration)
            parts[part] = pitches, note_durations
        return parts
    except:
        'File not found.'

def get_theme():
    parts = get_notes(FILE)

    for index, (part, (notes, note_durations)) in enumerate(parts.items()):
        print 'processing part {0} ...'.format(index)
        stream = music.stream.Stream()
        theme = find_theme(zip(notes, note_durations))
        for noise in theme:
            if type(noise[0]) == list:
                note = music.chord.Chord(noise[0])
            else:
                # print noise
                note = music.note.Note(noise[0])
            note.duration = noise[1]
            stream.append(note)
        if len(stream.pitches) != 0:
            pass
            # stream.write('midi', fp='{0}/{1}{2}.mid'.format(DIRECTORY, SONG, index))
        # print map(lambda note: (note[0], note[1].type), theme)

# song = corpus.parse(FILE)
# song.plot('pianoroll')
