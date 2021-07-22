def print_settings(settings: object):
    for key in settings.__dict__.keys():
        if settings.__dict__[key] and not key in ['by_experiment', 'experiments', 'by_session', 'sessions', 'by_prev_session', 'prev_session']:
            print(" {}: {}".format(key, settings.__dict__[key]))
    if settings.by_experiment: print(" - experiments: {}".format(settings.experiments))
    if settings.by_session: print(" - sessions: {}".format(settings.sessions))
    if settings.by_prev_session: print(" - # of prev sessions: {}".format(settings.prev_sessions))
    print('\n-----------------')