from opto_analysis.process_data.create_save_load_session import create_session
from settings.data_bank import all_data_entries
import numpy as np

def test_create_save_load_session():

    session_created = create_session(all_data_entries[0], create_new=True)
    session_loaded = create_session(all_data_entries[0], create_new=False)

    for created_entry, loaded_entry in zip(session_created.__dict__, session_loaded.__dict__):
        created_data = session_created.__dict__[created_entry]
        loaded_data  = session_loaded.__dict__[loaded_entry]

        if 'opto_analysis' in str(created_data.__class__):
            for created_sub_entry, loaded_sub_entry in zip(created_data.__dict__, loaded_data.__dict__):
                created_sub_data = created_data.__dict__[created_sub_entry]
                loaded_sub_data  = loaded_data.__dict__[loaded_sub_entry]
            
            assert (np.array(created_sub_data==loaded_sub_data)).all()

        else:
            assert created_data==loaded_data
