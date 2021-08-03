from opto_analysis.utils.directory import Directory
import os

def test_directory():
    base_folder = ".\\sample_data"
    experiment  = "block edge vectors"
    tracking_video_folder = Directory(base_folder, experiment=experiment, stim_type='laser', tracking_video=True).path
    assert tracking_video_folder==".\\sample_data\\trial clips\\__tracking__"
    assert os.path.isdir(tracking_video_folder)
    os.rmdir(tracking_video_folder)

    stimulus_video_folder = Directory(base_folder, experiment=experiment, stim_type='audio', tracking_video=False).path
    assert stimulus_video_folder==".\\sample_data\\trial clips\\block edge vectors\\escape videos"
    assert os.path.isdir(stimulus_video_folder)
    os.rmdir(stimulus_video_folder)
    
    stimulus_video_folder = Directory(base_folder, experiment=experiment, stim_type='laser', tracking_video=False).path
    assert stimulus_video_folder==".\\sample_data\\trial clips\\block edge vectors\\laser videos"
    assert os.path.isdir(stimulus_video_folder)
    os.rmdir(stimulus_video_folder)
    os.rmdir(".\\sample_data\\trial clips\\block edge vectors")
    os.rmdir(".\\sample_data\\trial clips")

    
