import sys
from opto_analysis.run import track_data
def run_track_data(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    track_data()
    
if __name__ == "__main__":
    sys.exit(run_track_data())