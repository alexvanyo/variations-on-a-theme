class Location:
    def __init__(self, measure, beat):
        self.measure = measure
        self.beat = beat
    def __str__(self):
        return 'Measure: {0}, Beat: {1}'.format(self.measure, self.beat)

class SongNote:
    def __init__(self, note, duration, location):
        self.note = note
        self.duration = duration
        self.location = Location(location[0], location[1])
    def __eq__(self, other):
        return (isinstance(other, SongNote) and 
                self.note == other.note and 
                self.duration == other.duration)
    def __str__(self):
        return 'Note: {0}, Duration: {1}, Location: ({2})'.format(self.note, self.duration.type, self.location)
