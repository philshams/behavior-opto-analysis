from dataclasses import dataclass

@dataclass(frozen=True)
class Processing_settings:
    create_new_registration: bool=False
    skip_registration: bool=True
    fisheye_correction_file: str=None
    size: int=1024
    pixels_per_cm : int=10
    by_experiment: bool=False
    experiments: list=None
    by_session: bool=False
    sessions: list=None
    by_prev_session: bool=False
    prev_session: list=None

@dataclass(frozen=True)
class Tracking_settings:
    dlc_settings_file: str = None
    inverse_fisheye_correction_file: str = None
    redo_dlc_tracking: bool=False
    redo_processing_step: bool=False
    skip_processing_step: bool=False
    display_tracking_output: bool=False
    min_confidence_in_tracking: float=None
    max_deviation_from_rest_of_points: int=None
    by_experiment: bool=False
    experiments: list=None
    by_session: bool=False
    sessions: list=None
    by_prev_session: bool=False
    prev_session: list=None

@dataclass(frozen=True)
class Visualization_settings:
    visualize_laser_trials: bool=True
    visualize_escape_trials: bool=True
    display_tracking:bool=False
    display_trail:bool=True
    rapid: bool=True
    display_stim_status: bool=True
    size: int=1024
    seconds_before_audio: int = 3
    seconds_before_laser: int = 3
    seconds_after_audio: int = 2
    seconds_after_laser: int = 6
    save_folder: str = None
    fisheye_correction_file: str = None
    generate_rendering: bool=False
    by_experiment: bool=False
    experiments: list=None
    by_session: bool=False
    sessions: list=None
    by_prev_session: bool=False
    prev_session: list=None

@dataclass(frozen=True)
class Analysis_settings:
    plot_type: str = None
    experiments: list = 'all'
    experiments_group_A: list = None
    experiments_group_B: list = None
    sessions: list = None
    sessions_group_A: list = None
    sessions_group_B: list = None
    prev_session_group_A: list = None # [0]
    prev_session_group_B: list = None # [1]
    by_experiment: bool=True
    by_session: bool=False
    by_prev_session: bool=False
