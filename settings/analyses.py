from opto_analysis.utils.settings_objects import Settings_analyze_local
analyses = {}

analyses["escapes"] = Settings_analyze_local(
    title='escapes trajectories', plot_escape = True, 
    by_session=True, sessions=[0,1])
    
analyses["laser"] = Settings_analyze_local(
    title='laser trajectories', plot_laser=True,
    by_session=True, sessions=[0,1])

analyses["escape targets"] = Settings_analyze_local(
    title='escape targets', plot_targets=True,
    by_session=True, sessions=[0,1])

analyses["escape targets compare"] = Settings_analyze_local(
    title='escape targets 1 vs 1+2', plot_targets=True,
    compare=True, by_session=True, 
    group_1 = [0], group_2=[0,1]) #, group_3 = [0], group_4=[0,1])


