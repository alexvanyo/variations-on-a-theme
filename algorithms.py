# longest repeated sub-sequence
import numpy 
def find_theme(notes):
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