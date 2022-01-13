databank = {}
# databank['path'] = ".\\sample_data\\"                          # sample data
databank['path'] = "D:\\Dropbox (UCL)\\DAQ\\upstairs_rig\\"      # full dataset

databank['session IDs'] = [
#-Session #s----Name of experiment-----prev session------Folder with data------
[0,0,      'block edge vectors',     False,        "9718_block evs"],
[1,1,      'block edge vectors',     False,        "9719_block evs"],
[2,2,      'block edge vectors',     False,        "9715_block evs"],
[3,3,      'block edge vectors',     False,        "9716_block evs"],
[4,4,      'block edge vectors',     True, "0365_block EVs + pinch"],
[5,5,      'block edge vectors',     True, "0361_block EVs + pinch"],
[6,6,      'block edge vectors',     True, "0360_block EVs + pinch"],
[7,7,      'block edge vectors',     True, "0357_block EVs + pinch"],

[8,0,      'block pre edge vectors',     False,    "9751_block pre evs"],
[9,1,      'block pre edge vectors',     False,    "9754_block pre evs"],
[10,2,     'block pre edge vectors',     False,    "9747_block pre evs"],
[11,3,     'block pre edge vectors',     False,    "0361_block pre EVs"],
[12,4,     'block pre edge vectors',     True,     "9709_block pre evs"],
[13,5,     'block pre edge vectors',     True,     "9716_block pre evs"],
[14,6,     'block pre edge vectors',     True,     "9711_block pre evs"],
[15,7,     'block pre edge vectors',     True,     "0364_block pre EVs"],

[16,0,  'block post edge vectors', False,   "9748_block post evs"],
[17,1,  'block post edge vectors', False,   "9750_block post evs"],
[18,2,  'block post edge vectors', False,   "9756_block post evs"],
[19,3,  'block post edge vectors', False,   "2758_block post evs"],
[20,4,  'block post edge vectors', True,    "9715_block post evs"],
[21,5,  'block post edge vectors', True,    "9716_block post evs"],
[22,6,  'block post edge vectors', True,    "9709_block post evs"],
[23,7,  'block post edge vectors', True,    "9711_block post evs"],

[24,0, 'block after 2nd edge vector', False, "0360_allow then block"],
[25,1, 'block after 2nd edge vector', False, "0356_allow then block"],
[26,2, 'block after 2nd edge vector', False, "0357_allow then block"],
[27,3, 'block after 2nd edge vector', False, "0358_allow then block"],
[28,4, 'block after 2nd edge vector', True,  "9756_allow then block"],
[29,5, 'block after 2nd edge vector', True,  "9758_allow then block"],
[30,6, 'block after 2nd edge vector', True,  "9751_allow then block"],
[31,7, 'block after 2nd edge vector', True,  "9754_allow then block"],

[32,0,      'no laser',     False,       "0359_obstacle removal"],
[33,1,      'no laser',     False,       "0362_obstacle removal"],
[34,2,      'no laser',     False,       "0363_obstacle removal"],
[35,3,      'no laser',     False,       "0364_obstacle removal"],
[36,4,      'no laser',     True,        "0360_obstacle removal"],
[37,5,      'no laser',     True,        "0365_obstacle removal"],
[38,6,      'no laser',     True,        "0367_obstacle removal"],
[39,7,      'no laser',     True,        "0357_obstacle removal"],

[40,0,      'open field',     False,       "9713_open field"],
[41,1,      'open field',     False,       "0365_open field"],
[42,2,      'open field',     False,       "0366_open field"],
[43,3,      'open field',     False,       "0367_open field"],
[44,4,      'open field',     True,        "0359_open field"],
[45,5,      'open field',     True,        "0358_open field"],
[46,6,      'open field',     True,        "0362_open field"],
[47,7,      'open field',     True,        "0363_open field"],

[48,0, 'laser place preference', True,  "9714_place pref left"],
[49,1, 'laser place preference', True,  "9717_place pref left"],
[50,2, 'laser place preference', True, "9719_place pref right"],
[51,3, 'laser place preference', True, "9709_place pref right"],
[52,4, 'laser place preference', True,  "9710_place pref left"],
[53,5, 'laser place preference', True, "9711_place pref right"],
[54,6, 'laser place preference', True,  "9715_place pref left"],
[55,7, 'laser place preference', True, "9716_place pref right"],

[56,0, 'laser power test I', True,  "0367_laser powers"],
[57,1, 'laser power test I', True,  "0363_laser powers"],
[58,2, 'laser power test I', True,  "0362_laser powers"],
[59,3, 'laser power test I', True,  "0358_laser powers"],

[60,0, 'initiation set I', False, "0654_initiation set"],
[61,1, 'initiation set I', False, "0658_initiation set"],
[62,2, 'initiation set I', False, "0655_initiation set"],
[63,3, 'initiation set I', False, "0656_initiation set"],
[64,4, 'initiation set I', False, "0651_initiation set"],
[65,5, 'initiation set I', False, "0652_initiation set"],
[66,6, 'initiation set I', False, "0653_initiation set"],
[67,7, 'initiation set I', False, "0657_initiation set"],

[68,0, 'initiation set II', False, "0660_south side"],
[69,1, 'initiation set II', False, "0661_south side"],
[70,2, 'initiation set II', False, "0655_south side"],
[71,3, 'initiation set II', False, "0662_south side"],
[72,4, 'initiation set II', False, "0651_south side"],
[73,5, 'initiation set II', False, "0653_south side"],
[74,6, 'initiation set II', False, "0658_south side"],
[75,7, 'initiation set II', False, "0656_south side"],

[76,0, 'initiation set I - obstacle', False, "0655_ISOB"],
[77,1, 'initiation set I - obstacle', False, "0660_ISOB"],
[78,2, 'initiation set I - obstacle', False, "0661_ISOB"],
[79,3, 'initiation set I - obstacle', False, "0662_ISOB"],
[80,4, 'initiation set I - obstacle', False, "0653_ISOB"],
[81,5, 'initiation set I - obstacle', False, "0656_ISOB"],
[82,6, 'initiation set I - obstacle', False, "0651_ISOB"],
[83,7, 'initiation set I - obstacle', False, "0658_ISOB"]

]