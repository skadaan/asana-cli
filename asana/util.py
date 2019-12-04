import configparser
import json
from os import path


DATA_FILE = 'data.ini'

file_exists = path.exists(DATA_FILE)


def convert_to_dict(string):
    list_ = []
    while True:
        i = string.find('},{') + 1
        if i == 0:
            break
        list_.append(string[:i])
        string = string[i+1:]
    list_.append(string)
    return [json.loads(l) for l in list_]


def add_to_data_file(section_name, **kwargs):
    try:
        config = configparser.ConfigParser()
        config[section_name] = kwargs
        with open(DATA_FILE, 'a') as configfile:
            config.write(configfile)
    except Exception as e:
        print(e)


def update_data_file(section_name, **kwargs):
    p = configparser.ConfigParser()
    with open(DATA_FILE, 'r+') as s:
        p.read_file(s)
        p.remove_section(section_name)
        s.seek(0)
        p.write(s)
        s.truncate()
    add_to_data_file(section_name, **kwargs)


def get_value_in_data_file(section, key):
    config = configparser.ConfigParser()
    config.read(DATA_FILE)
    return config.get(section, key)


def section_in_data_file():
    config = configparser.ConfigParser()
    config.read(DATA_FILE)
    return config.sections()
