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
            # move contents of Darshan_logs_txt folder to Darshan_logs_txt_old
            if not os.path.exists(folder + '/Darshan_logs_txt_old'):
                os.makedirs(folder + '/Darshan_logs_txt_old')
            else:
                print("Darshan_logs_txt_old folder already exists in " + folder)
        
            for darshan_log_txt in os.listdir(folder + '/Darshan_logs_txt'):
                os.rename(os.path.join(folder + '/Darshan_logs_txt', darshan_log_txt), os.path.join(folder + '/Darshan_logs_txt_old', darshan_log_txt))
        for txt_log in txt_logs:
            if txt_log.endswith('.json'):
                # remove json files
                os.remove(os.path.join(folder + '/Darshan_logs_txt', txt_log))
        # unpack each file
        
        for darshan_log in darshan_logs:
            if darshan_log.endswith('.json'):
                continue
            # unpack each file
            print("Unpacking " + darshan_log)
            print("darshan-dxt-parser --show-incomplete " + os.path.join(folder, 'Darshan_logs', darshan_log) + " > " + os.path.join(folder, 'Darshan_logs_txt', darshan_log.replace('.ini.darshan', '.txt')))
            subprocess.call("darshan-dxt-parser --show-incomplete " + os.path.join(folder, 'Darshan_logs', darshan_log) + " > " + os.path.join(folder, 'Darshan_logs_txt', darshan_log.replace('.ini.darshan', '.txt')), shell=True)
        

if __name__ == '__main__':
    unpack_all()
