import os
import sys
import subprocess

runable_sections = ['ior-easy', 'ior-hard', 'ior-rnd4K', 'ior-rnd1MB',
                    'mdworkbench', 'find-easy', 'find', 'find-hard',
                    'mdtest-easy', 'mdtest-hard']

# cd to all the directories and run commands in the run_commands.txt file
for section in runable_sections:
    print('Running commands in ' + section)
    os.chdir('..')
    with open(f'Trace_Dataset/{section}/run_commands.txt') as f:
        for line in f:
            print('\t running ' + line)
            subprocess.call(line, shell=True)
    os.chdir('Trace_Dataset')
