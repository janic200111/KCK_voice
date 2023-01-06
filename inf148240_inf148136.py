from __future__ import division
from matplotlib import pylab as plt
import numpy as np
import scipy.io.wavfile
from scipy.sig import kaiser, decimate
from copy import copy
import os, re
import sys

def analyze_wav(filename):
  sampling_rate, sig = scipy.io.wavfile.read(filename)
  smp_cnt = len(sig)
  duration = float(smp_cnt) / sampling_rate
  if not isinstance(sig[0], np.int16):
    sig = [s[0] for s in sig]
  sig = sig * kaiser(smp_cnt, 100)

  spc = np.log(abs(np.fft.rfft(sig)))
  hps = copy(spc)
  for h in np.arange(2, 6):
    dec = decimate(spc, h)
    hps[:len(dec)] += dec
  peak_start = 50 * duration
  peak = np.argmax(hps[int(peak_start):])
  verdict = (peak_start + peak) / duration

  return 'M' if verdict < 165 else 'K'


try:
  filename=os.path.basename(sys.argv[1])
  print(analyze_wav(filename))
except:
    print("K")