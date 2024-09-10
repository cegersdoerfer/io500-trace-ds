import configparser
import argparse
import json
import os
import glob
import subprocess

#runable_sections = ['ior-easy', 'ior-hard', 'ior-rnd4K', 'ior-rnd1MB', 'mdtest-easy', 'mdtest-hard']

runable_sections = ['ior-rnd1MB']

repetitions = 1

#runable_sections = ['mdtest-easy']

def delete_all_existing_ini_files(section):
    os.chdir(section)
    for file in os.listdir():
        if file.endswith('.ini'):
            os.remove(file)
    os.chdir('..')

if __name__ == '__main__':

    for section in runable_sections:
        if not os.path.isdir(section):
            os.mkdir(section)
        else:
            delete_all_existing_ini_files(section)
            print('deleted in in ' + section)
        # generate param combinations
        subprocess.call(['python3', 'param_combinations.py', '--section', section])
        print(f'Generated param combinations for {section}')
        # open combinations file
        with open(f"{section}/param_combinations.txt", "r") as f:
            combinations = f.readlines()
            for combination in combinations:
                print(combination)
                # create new congig file
                subprocess.call(['python3', 'create_config.py', '--enable', section, '--params', combination, '--file', 'config-all.ini', '--repititions', str(repetitions)])

    for section in runable_sections:
        if not os.path.isdir(f'{section}/Darshan_logs'):
            os.mkdir(f'{section}/Darshan_logs')
        else:
            files = glob.glob(f'{section}/Darshan_logs/*')
            for f in files:
                os.remove(f)
        with open(f'{section}/run_commands.txt', 'w') as f:
            for file in os.listdir(section):
                if file.endswith('.ini'):
                    f.write(f'./io500_ds.sh Trace_Dataset/{section}/{file} Trace_Dataset/{section}/Darshan_logs/{file}.darshan _ \n')

