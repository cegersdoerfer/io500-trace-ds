import os




sections = ['ior-easy', 'ior-hard', 'ior-rnd4K', 'ior-rnd1MB',
                   'mdworkbench', 'find-easy', 'find', 'find-hard',
                   'mdtest-easy', 'mdtest-hard']


def extract_run_time(file):
    # run time will always be represented as '# run time: 87.9674'
    with open(file, 'r') as f:
        for line in f:
            if line.startswith('# run time:'):
                return float(line.split(':')[1].strip())
    return None

file
for section in sections:
    darshan_log_reports = os.listdir(os.path.join(section, 'Darshan_logs_txt'))
    for report in darshan_log_reports:
        file = os.path.join(section, 'Darshan_logs_txt', report)
        run_time = extract_run_time(file)
        if run_time:
            print(section, report, run_time)
