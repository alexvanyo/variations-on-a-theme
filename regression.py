from music21 import corpus
import combined
import time
import os

timestamp = time.time()

for i in xrange(len(corpus.getBachChorales())):
    regression_stream = combined.simpleFileRandomizer(corpus.getBachChorales()[i])

    if not os.path.exists("regression\\" + str(i)):
        os.makedirs("regression\\" + str(i))

    regression_stream.write("midi", fp="regression\\" + str(i) + "\\" + str(timestamp) + ".mid")

print "Finished in " + str(time.time() - timestamp) + " seconds."
