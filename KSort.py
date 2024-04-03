import spikeinterface as si
import spikeinterface.extractors as se 
import spikeinterface.preprocessing as spre
import spikeinterface.sorters as ss
import spikeinterface.postprocessing as spost
import spikeinterface.qualitymetrics as sqm
import spikeinterface.comparison as sc
import spikeinterface.exporters as sexp
import spikeinterface.widgets as sw

print(f"SpikeInterface version: {si.__version__}")

import glob
import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess
from pathlib import Path

import warnings
warnings.simplefilter("ignore")

folders_ = ["D:\KILOSORT-DATA\Day52 Ens42 (dmPFC Caudate)",
            "D:\KILOSORT-DATA\Day53 Ens43 (dlPFC Caudate)",
            "D:\KILOSORT-DATA\Day54 Ens44 (dmPFC Caudate)",
            "D:\KILOSORT-DATA\Day55 Ens45 (dlPFC Caudate)"];

probes_ = [[2,1],
           [2,1],
           [2,1],
           [2,1]];

def run_ksort(dir,probe_,probe_type_):
    base_folder = Path(dir)
    file_list = list(base_folder.glob("*.xdat"))
    data_path = file_list[0]
    
    channel_gain = 5.0
    sorting_alg = 'kilosort3'
    
    recording_binary = si.read_binary(file_paths=data_path,sampling_frequency=30000.0,dtype='float32',num_chan=134)
    recording_binary.annotate(is_filtered=False)
    
    channel_ids = recording_binary.get_channel_ids()
    fs = recording_binary.get_sampling_frequency()
    num_chan = recording_binary.get_num_channels()
    num_segments = recording_binary.get_num_segments()
    
    print(f'Channel ids: {channel_ids}')
    print(f'Sampling frequency: {fs}')
    print(f'Number of channels: {num_chan}')
    print(f"Number of segments: {num_segments}")
    
    probe_A_channels = channel_ids[:64];
    probe_B_channels = channel_ids[64:128];
    
    if probe_ == 0:
        recording_to_process = recording_binary.channel_slice(channel_ids=probe_A_channels)
    else:
        recording_to_process = recording_binary.channel_slice(channel_ids=probe_B_channels)
    
    recording_scaled = spre.scale(recording_to_process, gain=channel_gain);
    recording_f = spre.bandpass_filter(recording_scaled, freq_min=300, freq_max=6000)
    recording_cmr = spre.common_reference(recording_f, reference='global', operator='median')
    
    fs = recording_cmr.get_sampling_frequency()
    #recording_sub = recording_cmr.frame_slice(start_frame=0*fs, end_frame=1500*fs)
    recording_sub = recording_cmr
    recording_sub
    
    job_kwargs = dict(n_jobs=10, chunk_duration="1s", progress_bar=True)
    
    if probe_ == 0:
        preprocessed_dir = base_folder / "probe_a" / "preprocessed"
    else:
        preprocessed_dir = base_folder / "probe_b" / "preprocessed"
    
    if preprocessed_dir.is_dir():
        recording_saved = si.load_extractor(preprocessed_dir)
    else:
        recording_saved = recording_sub.save(folder=preprocessed_dir, **job_kwargs)
    
    ss.Kilosort3Sorter.set_kilosort3_path('D:\Kilosort-main\Kilosort-main')
    ss.Kilosort2_5Sorter.set_kilosort2_5_path('D:\Kilosort-2.5')
    ss.Kilosort2Sorter.set_kilosort2_path('D:\Kilosort-2.0\Kilosort-2.0')
    
    sorter_params = {'do_correction': False}
    
    poly2_config = [
        [-21.5, -450],
        [-21.5, -500],
        [-21.5, -550],
        [-21.5, -600],
        [-21.5, -650],
        [-21.5, -700],
        [-21.5, -750],
        [-21.5, -800],
        [-21.5, -850],
        [-21.5, -900],
        [-21.5, -950],
        [-21.5, -1000],
        [-21.5, -1050],
        [-21.5, -1100],
        [-21.5, -1150],
        [-21.5, -1200],
        [-21.5, -100],
        [-21.5, -50],
        [-21.5, -200],
        [-21.5, -150],
        [-21.5, -300],
        [-21.5, -250],
        [-21.5, -400],
        [-21.5, -350],
        [-21.5, -1550],
        [-21.5, -1600],
        [-21.5, -1450],
        [-21.5, -1500],
        [-21.5, -1350],
        [-21.5, -1400],
        [-21.5, -1250],
        [-21.5, -1300],
        [21.75, -1325],
        [21.75, -1275],
        [21.75, -1425],
        [21.75, -1375],
        [21.75, -1525],
        [21.75, -1475],
        [21.75, -1625],
        [21.75, -1575],
        [21.75, -375],
        [21.75, -425],
        [21.75, -275],
        [21.75, -325],
        [21.75, -175],
        [21.75, -225],
        [21.75, -75],
        [21.75, -125],
        [21.75, -1225],
        [21.75, -1175],
        [21.75, -1125],
        [21.75, -1075],
        [21.75, -1025],
        [21.75, -975],
        [21.75, -925],
        [21.75, -875],
        [21.75, -825],
        [21.75, -775],
        [21.75, -725],
        [21.75, -675],
        [21.75, -625],
        [21.75, -575],
        [21.75, -525],
        [21.75, -475]
    ]
    
    edge100_config = [
        [129.62, -40],
        [129.62, -140],
        [129.62, -240],
        [129.62, -340],
        [129.62, -440],
        [129.62, -540],
        [129.62, -640],
        [129.62, -740],
        [129.62, -840],
        [129.62, -940],
        [129.62, -1040],
        [129.62, -1140],
        [129.62, -1240],
        [129.62, -1340],
        [129.62, -1440],
        [129.62, -1540],
        [129.62, -3040],
        [129.62, -3140],
        [129.62, -2840],
        [129.62, -2940],
        [129.62, -2640],
        [129.62, -2740],
        [129.62, -2440],
        [129.62, -2540],
        [129.62, -2240],
        [129.62, -2340],
        [129.62, -2040],
        [129.62, -2140],
        [129.62, -1840],
        [129.62, -1940],
        [129.62, -1640],
        [129.62, -1740],
        [129.62, -4640],
        [129.62, -4740],
        [129.62, -4440],
        [129.62, -4540],
        [129.62, -4240],
        [129.62, -4340],
        [129.62, -4040],
        [129.62, -4140],
        [129.62, -3840],
        [129.62, -3940],
        [129.62, -3640],
        [129.62, -3740],
        [129.62, -3440],
        [129.62, -3540],
        [129.62, -3240],
        [129.62, -3340],
        [129.62, -4840],
        [129.62, -4940],
        [129.62, -5040],
        [129.62, -5140],
        [129.62, -5240],
        [129.62, -5340],
        [129.62, -5440],
        [129.62, -5540],
        [129.62, -5640],
        [129.62, -5740],
        [129.62, -5840],
        [129.62, -5940],
        [129.62, -6040],
        [129.62, -6140],
        [129.62, -6240],
        [129.62, -6340]
    ]
    
    edge50_config = [
        [129.62, -40],
        [129.62, -90],
        [129.62, -140],
        [129.62, -190],
        [129.62, -240],
        [129.62, -290],
        [129.62, -340],
        [129.62, -390],
        [129.62, -440],
        [129.62, -490],
        [129.62, -540],
        [129.62, -590],
        [129.62, -640],
        [129.62, -690],
        [129.62, -740],
        [129.62, -790],
        [129.62, -1540],
        [129.62, -1590],
        [129.62, -1440],
        [129.62, -1490],
        [129.62, -1340],
        [129.62, -1390],
        [129.62, -1240],
        [129.62, -1290],
        [129.62, -1140],
        [129.62, -1190],
        [129.62, -1040],
        [129.62, -1090],
        [129.62, -940],
        [129.62, -990],
        [129.62, -840],
        [129.62, -890],
        [129.62, -2340],
        [129.62, -2390],
        [129.62, -2240],
        [129.62, -2290],
        [129.62, -2140],
        [129.62, -2190],
        [129.62, -2040],
        [129.62, -2090],
        [129.62, -1940],
        [129.62, -1990],
        [129.62, -1840],
        [129.62, -1890],
        [129.62, -1740],
        [129.62, -1790],
        [129.62, -1640],
        [129.62, -1690],
        [129.62, -2440],
        [129.62, -2490],
        [129.62, -2540],
        [129.62, -2590],
        [129.62, -2640],
        [129.62, -2690],
        [129.62, -2740],
        [129.62, -2790],
        [129.62, -2840],
        [129.62, -2890],
        [129.62, -2940],
        [129.62, -2990],
        [129.62, -3040],
        [129.62, -3090],
        [129.62, -3140],
        [129.62, -3190]
    ]
    
    if probe_type == 0:
        config_ = poly2_config
    elif probe_type == 1:
        config_ = edge100_config
    elif probe_type == 2:
        config_ = edge50_config
    
    recording_saved.set_channel_locations(config_)
    
    # run spike sorting on entire recording
    if probe_ == 0:
        output_folder = base_folder / 'probe_a' / sorting_alg
    else:
        output_folder = base_folder / 'probe_b' / sorting_alg
        
    sorting_KS3 = ss.run_sorter(sorting_alg, recording_saved,
                                 output_folder=output_folder,
                                 verbose=True, **sorter_params, **job_kwargs)
    
    if sorting_alg == 'kilosort3':
        # Update params.py to point to temp_wh.dat locally
        params_file = output_folder / 'params.py'
        
        with open(params_file,'r') as file_:
            params_ = file_.readlines()
        
        if params_:
            params_[0] = 'dat_path = \'temp_wh.dat\'\n'
            with open(params_file,'w') as file_:
                file_.writelines(params_)
    
        # Delete the unnecessary recording.dat if it exists
        tbd = output_folder / 'recording.dat'
        if os.path.exists(tbd):
            os.remove(tbd)
    
        # Extract phy waveforms
        phy_script = r'D:\SpikeInterface\run_phy.bat'
        subprocess.run([phy_script, output_folder])
    
        # Extract timing signal if not done already
        if not os.path.exists(base_folder / 'timestamps.data'):
            subprocess.run(['python','D:/SpikeInterface/extract_neuropixels.py',data_path])

for index,folder in enumerate(folders_):
    run_ksort(folder,0,probes_[index][0])
    run_ksort(folder,1,probes_[index][1])