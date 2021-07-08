import sys
from opto_analysis.run import run
def session(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    run()
    
if __name__ == "__main__":
    sys.exit(session())