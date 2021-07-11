import sys
from opto_analysis.run import analyze_data
def run_analyze_data(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    analyze_data()
    
if __name__ == "__main__":
    sys.exit(run_analyze_data())