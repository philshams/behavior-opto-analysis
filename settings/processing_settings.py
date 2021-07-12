from opto_analysis.settings_objects import Processing_settings

# select the analysis settings
processing_settings = Processing_settings(

    create_new_registration = False,
    skip_registration = True,

    # TODO: find out if nonzero x and y offset are needed

    by_experiment=False,
    experiments = [''],

    by_session=True,
    sessions=[0,1],

    by_prev_session=False,
    prev_session=[0],

)
