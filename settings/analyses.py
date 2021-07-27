from opto_analysis.utils.settings_objects import Settings_analyze_local
analyses = {}

analyses["escapes"] = Settings_analyze_local(
    title='escapes test', plot_escape = True, 
    by_session=True, sessions=[0,1])
    
analyses["laser"] = Settings_analyze_local(
    title='laser test', plot_laser=True,
    by_session=True, sessions=[0,1])

analyses["escape targets"] = Settings_analyze_local(
    title='escape targets', plot_targets=True,
    by_session=True, sessions=[0,1])


