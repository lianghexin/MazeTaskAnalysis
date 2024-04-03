import numpy as np
import sys

file_path = sys.argv[1]

timefile = file_path / 'timestamps.npy'
statefile = file_path / 'states.npy'
outfile = file_path / 'timestamps.data'

a = np.load(timefile)
b = np.load(statefile)

c = a[b==1]
c.shape = (c.size,1)

d = (a[b==-1]-a[b==1])*1000
d.shape = (d.size,1)

np.savetxt(outfile,np.hstack([c,d]),fmt='%.6f,%.1f')