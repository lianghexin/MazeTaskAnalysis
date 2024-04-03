import os
import numpy as np
import sys

file_path = sys.argv[1]
sample_rate = float(sys.argv[2]);
nchannels = int(sys.argv[3])
sync_channel = int(sys.argv[4])
bytes_per_sample = int(sys.argv[5])

if bytes_per_sample == 2:
    datatype = np.int16
elif bytes_per_sample == 4:
    datatype = np.float32
else:
    datatype = np.float64

# Read in bytes
if file_path:
    nsamples = os.path.getsize(file_path)/nchannels/bytes_per_sample
    sync = np.zeros(int(nsamples))
    count = 0
    with open(file_path, "rb") as file:
        while True:
            #Read in nchannels float values
            bytes = file.read(nchannels*bytes_per_sample)
            
            if not bytes:
                break;
            
            # Interpret as float
            data = np.frombuffer(bytes, dtype=datatype)
            
            sync[count] = data[sync_channel]

            count += 1
            if count % 30000 == 0:
                print("Progress: {:.2f}%".format(count/nsamples*100),end='\r')
    
    # Get indices of pulses
    ind = np.nonzero(sync)[0]
    
    # Get duration and timestamps of pulses
    dur = []
    ts = []
    last = ind[0]

    for i in range(2,len(ind)):
        if ind[i]-ind[i-1] > 1:
            dur.append(round((ind[i-1]-last)/15)/2)
            ts.append(last/sample_rate)
            last = ind[i]
    
    # Prepare the data to be saved
    a = np.array(ts)
    b = np.array(dur)
    a.shape = (a.size,1)
    b.shape = (b.size,1)
    
    # Save data in same directory as raw data
    np.savetxt(os.path.dirname(file_path)+"\\timestamps.data",np.hstack([a,b]),fmt='%.6f,%.6f')