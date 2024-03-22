import os
import sys
import subprocess
import json


def parse_rpc_stats(output):
    # Split the output into lines
    lines = output.split('\n')

    # Flag to mark when we are inside the 'pages per rpc' section
    in_pages_per_rpc_section = False

    # Store the results
    pages_per_rpc_data = {}

    # Current OST being processed
    current_ost = None

    for line in lines:
        # Check if line denotes a new OST
        if line.startswith('osc.'):
            current_ost = line.split('.')[1]  # Extract the OST identifier
            pages_per_rpc_data[current_ost] = {}

        # Check for the start of the 'pages per rpc' section
        if 'pages per rpc' in line:
            in_pages_per_rpc_section = True
            continue  # Skip the header line

        # Check for the end of the 'pages per rpc' section
        if in_pages_per_rpc_section and not line.strip():
            in_pages_per_rpc_section = False
            continue

        # Extract data if we are in the 'pages per rpc' section
        if in_pages_per_rpc_section and current_ost is not None:
            parts = line.split()
            page_size = parts[0].rstrip(':')  # Remove the colon
            read_data = parts[1:4]  # Extract read data
            write_data = parts[5:8]  # Extract write data

            # Store the data in the dictionary
            pages_per_rpc_data[current_ost][page_size] = {
                'read': {
                    'count': int(read_data[0]),
                    'percent': float(read_data[1]),
                    'cumulative_percent': float(read_data[2])
                },
                'write': {
                    'count': int(write_data[0]),
                    'percent': float(write_data[1]),
                    'cumulative_percent': float(write_data[2])
                }
            }

    return pages_per_rpc_data

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

runable_sections = ['ior-hard', 'ior-rnd4K', 'ior-rnd1MB',
                   'mdworkbench']
#runable_sections = ['mdtest-easy']

# cd to all the directories and run commands in the run_commands.txt file
for section in runable_sections:
    print('Running commands in ' + section)
    os.chdir('..')
    with open(f'Trace_Dataset/{section}/run_commands.txt') as f:
        for line in f:
            print('\t clearing stats')
            subprocess.call('lctl set_param osc.IOLustre*.rpc_stats=0', shell=True)
            print('\t running ' + line)
            subprocess.call(line, shell=True)
            output = subprocess.check_output(['lctl', 'get_param', 'osc.IOLustre*.rpc_stats'], text=True)
            #rpc_stats = parse_rpc_stats(output)
            #print(rpc_stats)
            #save_to_json(line.split(' ')[2]+'_results.json', rpc_stats)
            #subprocess.call('lctl set_param ldlm.namespaces.*.lru_size=clear', shell=True)

    os.chdir('Trace_Dataset')
