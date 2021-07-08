from dataclasses import dataclass
@dataclass(frozen=True)

class Options:
    process_data: bool=False
    run_DLC_tracking: bool=False
    run_analysis: bool=False
    analyze_particular_experiments: bool=False
    experiments_to_analyze: list=None
    analyze_particular_sessions: bool=False
    sessions_to_analyze: list=None
    analyze_particular_naivete: bool=False
    num_previous_sessions_to_analyze: list=None