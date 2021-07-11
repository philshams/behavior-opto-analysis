from dataclasses import dataclass

@dataclass(frozen=True)
class Processing_settings:
    create_new_metadata: bool=True
    examine_laser_trials: bool=False
    examine_audio_trials: bool=False
    rapid: bool=False
    dlc_tracking: bool=False
    dlc_settings_file: str=None
    analysis: bool=False
    by_experiment: bool=False
    experiments: list=None
    by_session: bool=False
    sessions: list=None
    by_prev_session: bool=False
    prev_session: list=None

@dataclass(frozen=True)
class Tracking_settings:
    dlc_settings_file: str = None
    by_experiment: bool=False
    experiments: list=None
    by_session: bool=False
    sessions: list=None
    by_prev_session: bool=False
    prev_session: list=None

@dataclass(frozen=True)
class Analysis_settings:
    plot_type: str = None
    experiments: list = None
    experiments_group_A: list = None
    experiments_group_B: list = None
    sessions: list = None
    sessions_group_A: list = None
    sessions_group_B: list = None
    prev_session_group_A = [0]
    prev_session_group_B = [1]
