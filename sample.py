import music21 as music
from algorithms import *
from AndyTestFileVariations import getPartsInfo
from SongNote import SongNote
import os

SONG = 'mary'
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
        parts2 = {}
        for part in song_file.parts:
            measure, beat = 1, 0
            pitches = []
            note_durations = []
            songNotes = []
            for note in part.flat.notes:
                note_duration = music.duration.convertTypeToNumber(note.duration.type)
                if type(note) == music.chord.Chord:
                    pitches.append(note.pitchNames)
                    songNotes.append(SongNote(note.pitchNames, note.duration, (measure, beat)))
                elif type(note) == music.note.Note:
                    pitches.append(note.nameWithOctave)
                    songNotes.append(SongNote(note.nameWithOctave, note.duration, (measure, beat)))
                elif type(note) == music.note.Rest:
                    pitches.append(note.fullName)
                    songNotes.append(SongNote(note.fullName, note.duration, (measure, beat)))
                note_durations.append(note.duration)
                beat += 1/note_duration
                if beat >= 1:
                    how_much_over = int(beat)
                    measure += (beat - how_much_over)
                    beat -= how_much_over
            parts2[part] = songNotes
            parts[part] = pitches, note_durations
        return parts2
    except Exception as exception:
        print exception
        print 'File not found.'



def get_theme2():
    parts = get_notes(FILE)

    for index, (part, songNotes) in enumerate(parts.items()):
        print 'processing part {0} ...'.format(index)
        notes = map(lambda x: x.note, songNotes)
        note_durations = map(lambda x: x.duration, songNotes)
        stream = music.stream.Stream()
        theme = find_theme(songNotes)
        for noise in theme:
            if type(noise.note) == list:
                note = music.chord.Chord(noise.note)
            else:
                # print noise
                note = music.note.Note(noise.note)
            note.duration = noise.duration
            stream.append(note)
        if len(stream.pitches) != 0:
            pass
            # stream.write('midi', fp='{0}/{1}{2}.mid'.format(DIRECTORY, SONG, index))
        print map(str, theme)


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
        print map(lambda note: (note[0], note[1].type), theme)

# song = corpus.parse(FILE)
# song.plot('pianoroll')
get_theme2()
