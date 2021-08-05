databank = {}
# databank['path'] = ".\\sample_data\\"                          # sample data
databank['path'] = "D:\\Dropbox (UCL)\\DAQ\\upstairs_rig\\"      # full dataset

databank['session IDs'] = [
#-Session #s----Name of experiment-----prev session------Folder with data------
    [0,0,      'block edge vectors',     False,       "21MAR16_9718_block evs"],
    [1,1,      'block edge vectors',     False,       "21MAR17_9719_block evs"],
    [2,2,      'block edge vectors',     False,       "21MAR17_9715_block evs"],
    [3,3,      'block edge vectors',     False,       "21MAR17_9716_block evs"],
    [4,4,      'block edge vectors',     True,        "21APR10_9751_block evs"],
    [5,5,      'block edge vectors',     True,        "21APR10_9753_block evs"],
    [6,6,      'block edge vectors',     True,        "21APR10_9747_block evs"],
    [7,7,      'block edge vectors',     True,        "21APR10_9748_block evs"],

    [8,0,      'block pre edge vectors',     False,    "21APR01_9751_block pre evs"],
    [9,1,      'block pre edge vectors',     False,    "21APR01_9753_block pre evs"], # MSSNG FRAMES
    [10,2,     'block pre edge vectors',     False,    "21APR01_9754_block pre evs"],
    [11,3,     'block pre edge vectors',     False,    "21APR01_9747_block pre evs"],
    [12,4,     'block pre edge vectors',     True,     "21APR01_9709_block pre evs"],
    [13,5,     'block pre edge vectors',     True,     "21APR01_9716_block pre evs"],
    [14,6,     'block pre edge vectors',     True,     "21APR01_9711_block pre evs"],
    # [15,7,     'block pre edge vectors',     True,     ""],

    [16,0,      'block post edge vectors',     False,       "21APR05_9748_block post evs"],
    [17,1,      'block post edge vectors',     False,       "21APR05_9750_block post evs"],
    [18,2,      'block post edge vectors',     False,       "21APR06_9756_block post evs"],
    [19,3,      'block post edge vectors',     False,       "21APR06_9758_block post evs"],
    [20,4,      'block post edge vectors',     True,        "21MAR22_9715_block post evs"],
    [21,5,      'block post edge vectors',     True,        "21MAR22_9716_block post evs"],
    [22,6,      'block post edge vectors',     True,        "21MAR23_9709_block post evs"],
    [23,7,      'block post edge vectors',     True,        "21MAR23_9711_block post evs"],

    # [24,0,      'block after 2nd edge vector',     False,       ""],
    # [25,1,      'block after 2nd edge vector',     False,       ""],
    # [26,2,      'block after 2nd edge vector',     False,       ""],
    # [27,3,      'block after 2nd edge vector',     False,       ""],
    [28,4,      'block after 2nd edge vector',     True,        "21APR12_9756_allow then block"],
    [29,5,      'block after 2nd edge vector',     True,        "21APR12_9758_allow then block"],
    [30,6,      'block after 2nd edge vector',     True,        "21APR17_9751_allow then block"],
    [31,7,      'block after 2nd edge vector',     True,        "21APR17_9754_allow then block"],

    # [32,0,      'no laser',     False,       ""],
    # [33,1,      'no laser',     False,       ""],
    # [34,2,      'no laser',     False,       ""],
    # [35,3,      'no laser',     False,       ""],
    # [36,4,      'no laser',     True,        ""],
    # [37,5,      'no laser',     True,        ""],
    # [38,6,      'no laser',     True,        ""],
    # [39,7,      'no laser',     True,        ""],

    [40,0,      'open field',     False,       "21MAR18_9713_open field"],
    # [41,1,      'open field',     False,       ""],
    # [42,2,      'open field',     False,       ""],
    # [43,3,      'open field',     False,       ""],
    # [44,4,      'open field',     True,       ""],
    # [45,5,      'open field',     True,       ""],
    # [46,6,      'open field',     True,       ""],
    # [47,7,      'open field',     True,       ""],

    [48,0, 'laser place preference (match expt parameters)', True, "21MAR27_9714_place pref left"],
    [49,1, 'laser place preference (match expt parameters)', True, "21MAR27_9717_place pref left"],
    [50,2, 'laser place preference (match expt parameters)', True, "21MAR27_9719_place pref right"],
    [51,3, 'laser place preference (match expt parameters)', True, "21MAR28_9709_place pref right"],
    [52,4, 'laser place preference (match expt parameters)', True, "21MAR28_9710_place pref left"],
    [53,5, 'laser place preference (match expt parameters)', True, "21MAR28_9711_place pref right"],
    [54,6, 'laser place preference (match expt parameters)', True, "21MAR28_9715_place pref left"],
    [55,7, 'laser place preference (match expt parameters)', True, "21MAR28_9716_place pref right"],

    [56,0, 'laser place preference (match loom parameters)', True, "21APR12_9751_place pref left"],
    [57,1, 'laser place preference (match loom parameters)', True, "21APR12_9754_place pref right"],
    [58,2, 'laser place preference (match loom parameters)', True, "21APR17_9747_place pref left"],
    [59,3, 'laser place preference (match loom parameters)', True, "21APR17_9748_place pref right"],
    [60,4, 'laser place preference (match loom parameters)', True, "21APR17_9750_place pref right"],
    [61,5, 'laser place preference (match loom parameters)', True, "21APR17_9753_place pref left"],
    [62,6, 'laser place preference (match loom parameters)', True, "21APR17_9755_place pref left"],
    [63,7, 'laser place preference (match loom parameters)', True, "21APR17_9756_place pref right"],

    [64,0, 'loom place preference', True,  "21APR08_9709_place pref right"],
    [65,1, 'loom place preference', True,  "21APR08_9710_place pref left"],
    [66,2, 'loom place preference', True,  "21APR08_9711_place pref right"],
    [67,3, 'loom place preference', True,  "21APR08_9713_place pref left"],
    [68,4, 'loom place preference', True,  "21APR08_9714_place pref left"],
    [69,5, 'loom place preference', True,  "21APR08_9715_place pref left"],
    [70,6, 'loom place preference', True,  "21APR08_9716_place pref right"],
    [71,7, 'loom place preference', True,  "21APR08_9720_place pref right"],

]