import argparse
import itertools

# Define the ranges for each parameter
api_values = ['POSIX', 'MPIIO']
block_size_values = ['1073741824']
transfer_size_values = ['2K', '4K', '1MB', '4MB']
file_per_proc_values = ["True", "False"]
unique_dir_values = ["True"]#["True", "False"]
random_prefill_values = ['0']#['0', '1024']
n_values = ['100000']
waiting_time_values = ['0.0']#['0.0', '0.5', '1.0']
precreate_per_set_values = ['10']#['10', '100', '1000']
files_per_proc_values = ['10']#, '100', '1000']
nproc_values = ['1']#, '10', '100']
pfind_queue_length_values = ['10000']#['1000', '10000', '100000']
pfind_steal_next_values = ["False"]#["True", "False"]
pfind_parallelize_values = ["False"]#["True", "False"]
segment_count_values = ['100000']
collective_values = ["True", "False"]
files_per_dir_values = ['']#, '100', '1000']
def main():
    parser = argparse.ArgumentParser(description='Generate parameter combinations for a specific configuration section.')
    parser.add_argument('--section', help='Name of the configuration section')
    args = parser.parse_args()

    def generate_combinations_for_section(section_name, params):
        param_keys = params.keys()
        combinations = list(itertools.product(*params.values()))
        return [
            {section_name: dict(zip(param_keys, combo))}
            for combo in combinations
        ]

    section_combinations = {
        "ior-easy": generate_combinations_for_section(
            "ior-easy", {
                'api': api_values, 'blockSize': block_size_values, 'transferSize': transfer_size_values,
                'filePerProc': file_per_proc_values, 'uniqueDir': unique_dir_values
            }
        ),
        "ior-rnd4K": generate_combinations_for_section(
            "ior-rnd4K", {
                'api': api_values, 'blockSize': block_size_values, 'randomPrefill': random_prefill_values
            }
        ),
        "mdtest-easy": generate_combinations_for_section(
            "mdtest-easy", {
                'api': api_values, 'n': n_values
            }
        ),
        "ior-rnd1MB": generate_combinations_for_section(
            "ior-rnd1MB", {
                'api': api_values, 'blockSize': block_size_values, 'randomPrefill': random_prefill_values
            }
        ),
        "mdworkbench": generate_combinations_for_section(
            "mdworkbench", {
                'api': api_values, 'waitingTime': waiting_time_values, 'precreatePerSet': precreate_per_set_values, 
                'filesPerProc': files_per_proc_values
            }
        ),
        "find-easy": generate_combinations_for_section(
            "find-easy", {
                'nproc': nproc_values, 'pfindQueueLength': pfind_queue_length_values, 
                'pfindStealNext': pfind_steal_next_values, 'pfindParallelize': pfind_parallelize_values
            }
        ),
        "ior-hard": generate_combinations_for_section(
            "ior-hard", {
                'api': api_values, 'segmentCount': segment_count_values, 'collective': collective_values
            }
        ),
        "mdtest-hard": generate_combinations_for_section(
            "mdtest-hard", {
                'api': api_values, 'n': n_values, 'filesPerDir': files_per_dir_values
            }
        ),
        "find": generate_combinations_for_section(
            "find", {
                'nproc': nproc_values, 'pfindQueueLength': pfind_queue_length_values, 
                'pfindStealNext': pfind_steal_next_values, 'pfindParallelize': pfind_parallelize_values
            }
        ),
        "find-hard": generate_combinations_for_section(
            "find-hard", {
                'nproc': nproc_values, 'pfindQueueLength': pfind_queue_length_values, 
                'pfindStealNext': pfind_steal_next_values, 'pfindParallelize': pfind_parallelize_values
            }
        )
    }

    selected_section = args.section
    if selected_section in section_combinations:
        print(f"Combinations for {selected_section}:")
        with open(f"{selected_section}/param_combinations.txt", "w") as file:
       	    for combo in section_combinations[selected_section]:
                print(combo)
                if selected_section == 'ior-easy':
                    if combo[selected_section]['api'] == 'MPIIO' and combo[selected_section]['filePerProc'] == 'True':
                        continue
                file.write(f"{combo}\n")
    else:
        print(f"Section '{selected_section}' not found.")

if __name__ == "__main__":
    main()

