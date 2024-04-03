D:
cd /d %1
call conda activate phy2
phy extract-waveforms params.py
conda deactivate
                