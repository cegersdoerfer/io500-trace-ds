import os
import pandas as pd

def create_file_table(directory):
    # Dictionary to hold file occurrences
    file_dict = {}

    # List of all folders
    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

    # Traverse each folder and list files
    for folder in folders:
        folder_path = os.path.join(directory, folder)
        for file in os.listdir(folder_path):
            if file.endswith('.txt'):
                if file not in file_dict:
                    file_dict[file] = []
                file_dict[file].append(folder)

    # Create a DataFrame
    df = pd.DataFrame(columns=folders)

    # Fill the DataFrame
    for file, folder_list in file_dict.items():
        df.loc[file] = [folder in folder_list for folder in folders]

    return df

# Specify your top-level directory here
top_level_directory = '.'
df = create_file_table(top_level_directory)

# Display the table
print(df)

# Optionally, save the table to a CSV file
df.to_csv('io_issues_table.csv')
