def print_settings(settings: object):
    for key in settings.__dict__.keys():
        if settings.__dict__[key] and not key in ['by_experiment', 'experiments', 'by_session', 'sessions', 'by_prev_session', 'prev_session']:
            print(" {}: {}".format(key, settings.__dict__[key]))
    if settings.by_experiment:      print(" - experiments: {}".format(settings.experiments))
    if settings.by_session:         print(" - sessions: {}".format(settings.sessions))
    if settings.by_prev_session:    print(" - # of prev sessions: {}".format(settings.prev_sessions))

def print_settings_analysis(settings: object):
    for key in settings.__dict__.keys():
        if settings.__dict__[key] and not key in ['analysis']:
            print(" {}: {}".format(key, settings.__dict__[key]))
    settings = settings.analysis
    if not settings.compare:
        if settings.by_experiment:      print(" - experiments: {}".format(settings.experiments))
        if settings.by_session:         print(" - sessions: {}".format(settings.sessions))
        if settings.by_prev_session:    print(" - # of prev sessions: {}".format(settings.prev_sessions))
    if settings.compare:
        if settings.by_experiment: 
            group_A_members = settings.experiments_group_A    
            group_B_members = settings.experiments_group_B
        if settings.by_session:       
            group_A_members = settings.sessions_group_A    
            group_B_members = settings.sessions_group_B  
        if settings.by_prev_session:   
            group_A_members = settings.prev_session_group_A    
            group_B_members = settings.prev_session_group_B 
        print(" - group A: {}\n - group B: {}".format(group_A_members, group_B_members))