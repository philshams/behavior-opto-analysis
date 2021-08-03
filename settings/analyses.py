from opto_analysis.utils.settings_objects import Settings_analyze_local
analyses = {}

analyses["escapes"] = \
    Settings_analyze_local( title='escapes trajectories - BLOCK', 
                            plot_escape = True, 
                            by_experiment=True, 
                            experiments=['block edge vectors'])
    
analyses["laser"] = \
    Settings_analyze_local( title='laser trajectories', 
                            plot_laser=True,
                            by_experiment=True, 
                            experiments=['block edge vectors'])

analyses["escapes PRE"] = \
    Settings_analyze_local( title='escapes trajectories - BLOCK PRE', 
                            plot_escape = True, 
                            by_experiment=True, 
                            experiments=['block pre edge vectors'])

analyses["escapes POST"] = \
    Settings_analyze_local( title='escapes trajectories - BLOCK POST', 
                            plot_escape = True, 
                            by_experiment=True, 
                            experiments=['block post edge vectors'])

analyses["escape targets EV vs PRE vs POST"] = \
    Settings_analyze_local( title='escape targets EV vs PRE vs POST', 
                            plot_targets=True,
                            compare=True, 
                            by_experiment=True, 
                            group_1 = ['block edge vectors'], 
                            group_2 = ['block pre edge vectors'], 
                            group_3 = ['block post edge vectors'])


