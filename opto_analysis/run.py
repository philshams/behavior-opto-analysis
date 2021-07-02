from opto_analysis.verify_time_sync import verify_time_sync

# set file paths
folder_prefix = "C:\\Users\\philip\\Dropbox (UCL - SWC)\\DAQ\\upstairs_rig\\"
file_paths = ["21MAR16_9718_block evs", 
              "21MAR17_9719_block evs"]

verify_time_sync(folder_prefix, file_paths)