import sys
from opto_analysis.run import process_data
def session(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    process_data()
    
if __name__ == "__main__":
    sys.exit(session())