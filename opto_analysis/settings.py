from dataclasses import dataclass

@dataclass(frozen=True)
class Analysis_settings:
    load_metadata: bool=True
    verify_data_sync: bool=False
    dlc_tracking: bool=False
    analysis: bool=False
    by_experiment: bool=False
    experiments: list=None
    by_session: bool=False
    sessions: list=None
    by_prev_session: bool=False
    prev_session: list=None


@dataclass(frozen=True)
class Plotting_settings:
    plot_type: str = None
    experiment_0: str = None
    experiment_1: str = None
    experiment_2: str = None
    experiment_3: str = None
    experiment_4: str = None
    experiment_5: str = None
    experiment_6: str = None
    experiment_7: str = None
    experiment_8: str = None
    experiment_9: str = None
    groups: list = None
