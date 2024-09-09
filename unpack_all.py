import subprocess
import os
import sys


def unpack_all():
    # find all folders in the current directory
    folders = [f for f in os.listdir('.') if os.path.isdir(f)]
    for folder in folders:
        # check if Darshan_logs folder exists
        if not os.path.exists(folder + '/Darshan_logs'):
            print("Darshan_logs folder does not exist in " + folder)
            continue
        # list all files in Darshan_logs folder in each folder
        darshan_logs = os.listdir(folder + '/Darshan_logs')
        txt_logs = os.listdir(folder + '/Darshan_logs_txt')
        # create Darshan_logs_txt folder if it does not exist
        if not os.path.exists(folder + '/Darshan_logs_txt'):
            os.makedirs(folder + '/Darshan_logs_txt')
        else:
            print("Darshan_logs_txt folder already exists in " + folder)
            # remove contents of Darshan_logs_txt folder
            for log in txt_logs:
                try:
                    os.remove(os.path.join(folder + '/Darshan_logs_txt', log))
                except:
                    continue
                    
        for txt_log in txt_logs:
            if txt_log.endswith('.json'):
                # remove json files
                try:
                    os.remove(os.path.join(folder + '/Darshan_logs_txt', txt_log))
                except:
                    continue
        # unpack each file
        
        for darshan_log in darshan_logs:
            if darshan_log.endswith('.json'):
                continue
            # unpack each file
            print("Unpacking " + darshan_log)
            print("darshan-parser --show-incomplete " + os.path.join(folder, 'Darshan_logs', darshan_log) + " > " + os.path.join(folder, 'Darshan_logs_txt', darshan_log.replace('.ini.darshan', '.txt')))
            subprocess.call("darshan-parser --show-incomplete " + os.path.join(folder, 'Darshan_logs', darshan_log) + " > " + os.path.join(folder, 'Darshan_logs_txt', darshan_log.replace('.ini.darshan', '.txt')), shell=True)
        

if __name__ == '__main__':
    unpack_all()
