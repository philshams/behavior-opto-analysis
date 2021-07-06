from opto_analysis.verify_time_sync import verify_time_sync

# set file paths
folder_prefix = "C:\\Users\\philip\\Dropbox (UCL - SWC)\\DAQ\\upstairs_rig\\"
file_paths = ["21MAR16_9718_block evs", 
              "21MAR17_9719_block evs"]

fps = 40
DAQ_sampling_rate = 15000

# for folder_path in [folder_prefix + fp for fp in file_paths]:

verify_time_sync(file_path, fps, DAQ_sampling_rate)