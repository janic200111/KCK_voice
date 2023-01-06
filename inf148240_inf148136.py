from __future__ import division
from matplotlib import pylab as plt
import numpy as np
import scipy.io.wavfile
from scipy.signal import kaiser, decimate
from copy import copy
import os, re
import sys

def analyze_wav(filename):
  sampling_rate, signal = scipy.io.wavfile.read(filename)
  samples_count = len(signal)
  duration = float(samples_count) / sampling_rate
  if not isinstance(signal[0], np.int16):
    signal = [s[0] for s in signal]
  signal = signal * kaiser(samples_count, 100)

  spectrum = np.log(abs(np.fft.rfft(signal)))
  hps = copy(spectrum)
  for h in np.arange(2, 6):
    dec = decimate(spectrum, h)
    hps[:len(dec)] += dec
  peak_start = 50 * duration
  peak = np.argmax(hps[int(peak_start):])
  fundamental = (peak_start + peak) / duration

  return 'M' if fundamental < 165 else 'K'


try:
  filename=os.path.basename(sys.argv[1])
  print(analyze_wav(filename))
except:
    print("K")