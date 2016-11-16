from music21 import corpus
import combined
import time
import os
from joblib import *


def parallel(f, args_list, n_jobs=-1, debug=False, **constant_args):
    resps = []
    if debug:
        for i in args_list:
            resps.append(f(i))
    else:
        with Parallel(n_jobs=n_jobs, verbose=5) as parallela:
            resps = (parallela((delayed(f)(args, **constant_args) for args in args_list)))
    return resps

def run_regression(song_name, time_stamp):
    processed_stream = combined.simpleFileRandomizer(song_name)

    file_path = "regression/" + song_name.split(os.path.sep)[-1]

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    processed_stream.write("midi", fp=file_path + "/" + str(time_stamp) + ".mid")

if __name__ == '__main__':
    parallel(run_regression, corpus.getBachChorales(), time_stamp=time.time())