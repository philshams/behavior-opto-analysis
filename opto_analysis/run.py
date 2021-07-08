from settings import program_name, program
from opto_analysis.process_data.select_sessions import select_sessions_to_analyze

def run():
    print("\n------ {} ------ \n{}".format(program_name, program))
    sessions_to_analyze = select_sessions_to_analyze(program)



if __name__=="__main__":
    run()