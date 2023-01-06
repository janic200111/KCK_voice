from __future__ import division
import numpy as np
import scipy.io.wavfile
from scipy.signal import kaiser, decimate
from copy import deepcopy
import os
import sys


def absolute_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def analyze_wav(filename):
    sampling_rate, sig = scipy.io.wavfile.read(filename)
    smp_cnt = len(sig)
    duration = float(smp_cnt) / sampling_rate
    if not isinstance(sig[0], np.int16):
        sig = [s[0] for s in sig]
    sig = sig * kaiser(smp_cnt, 100)

    spc = np.log(abs(np.fft.rfft(sig)))
    hps = deepcopy(spc)
    for h in range(2, 6):
        dec = decimate(spc, h)
        hps[:len(dec)] += dec
    peak_start = 50 * int(duration)
    peak = np.argmax(hps[peak_start:])

    return 'M' if (peak_start + peak) / duration < 165 else 'K'


# recognized = 0
# directory = "trainall"
# files = absolute_file_paths(directory)
# for file in files:
#     if analyze_wav(file) == file[-5]:
#         recognized += 1
# print(recognized)

try:
    filename = os.path.basename(sys.argv[1])
    print(analyze_wav(filename))
except:
    print("K")
