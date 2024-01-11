import configparser
import argparse
import json
import os

def read_ini_file(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def update_config_sections(config, enable_sections, params):
    # Disable all sections by default
    for section in config.sections():
        if 'run' in config[section]:
            config[section]['run'] = 'FALSE'
    
    # Enable specified sections and update parameters
    for section in enable_sections:
        if section in config:
            config[section]['run'] = 'TRUE'
            if section in params:
                for key, value in params[section].items():
                    config[section][key] = value

def write_ini_file(config, file_path):
    with open(file_path, 'w') as configfile:
        config.write(configfile)

def parse_parameters(param_str):
    try:
        # Convert the parameter string into a dictionary
        params = json.loads(param_str)
        if not isinstance(params, dict):
            raise ValueError("Parameters must be a dictionary.")
        return params
    except json.JSONDecodeError:
        raise ValueError("Invalid parameter format. Please provide a valid JSON string.")

def main():
    parser = argparse.ArgumentParser(description='Update INI file sections and parameters.')
    parser.add_argument('--enable', nargs='+', help='List of sections to enable', required=True)
    parser.add_argument('--params', type=parse_parameters, help='JSON string of parameters to update (e.g. \'{"ior-easy": {"transferSize": "4m"}}\')')
    parser.add_argument('--file', help='Path to the INI file', required=True)
    
    args = parser.parse_args()

    config = read_ini_file(args.file)
    update_config_sections(config, args.enable, args.params if args.params else {})
    # convert list of enabled sections to a string
    enabled_sections = '_'.join(args.enable)
    # check if dir named enabled_sections exists
    if not os.path.isdir(enabled_sections):
        os.mkdir(enabled_sections)
    # name the file based on params
    if args.params:
        param_str = ''
        for key, value in args.params.items():
            for param_key, param_value in value.items():
                param_str += f'{param_key}_{param_value}_'
        print(f'param str: {param_str}')
        param_str = '_'.join(args.enable) + '_' + param_str
        write_location = f'{enabled_sections}/{param_str}.ini'
    else:
        write_location = f'{enabled_sections}/default.ini'
    write_ini_file(config, write_location)

    print("Configuration updated successfully.")

if __name__ == "__main__":
    main()

