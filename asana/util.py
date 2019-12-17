import configparser
import json
from json import JSONDecodeError
import os
import csv

import yaml
dirname = os.path.dirname(__file__)
DATA_FILE = os.path.join(dirname, 'data.ini')

TASKS_FILE = os.path.join(dirname, 'tasks.json')

# DATA_FILE = 'data.ini'
#
# TASKS_FILE = 'tasks.txt'

file_exists = os.path.exists(DATA_FILE)


def file_exists(file=DATA_FILE):
    return os.path.exists(file)


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
    """
    retrieve the value of a key in a section
    :param section: section to search in
    :param key: key to retrieve the value of
    :return: value of 'key'
    """
    config = configparser.ConfigParser()
    config.read(DATA_FILE)
    return config.get(section, key)


def section_in_data_file():
    """
    :return: a list of all sections in the data.ini file
    """
    config = configparser.ConfigParser()
    config.read(DATA_FILE)
    return config.sections()


def add_to_task_file(tasks
        # section_id, section_gid, task_id, task
):
    if not file_exists(TASKS_FILE):
        f = open(TASKS_FILE, 'w')
        f.close()
    with open(TASKS_FILE, 'r+') as json_file:
        try:
            data = json.loads(json_file.read())
        except Exception:
            data = dict()

        # section = [section for section in list(data.keys()) if section_gid == section.strip(f'(S{section_id}) ')]
        # if section:
        #     data[section[0]].append({f'(T{task_id})': task})
        # else:
        #     data.update({f'(S{section_id}) {section_gid}': [{f'(T{task_id})': task}]})
        json_file.seek(0)
        json.dump(tasks, json_file)
        json_file.truncate()


def read_from_task_file():
    with open(TASKS_FILE, 'r') as f:
        data = json.load(f)
    return data

def get_task_from_tasks_file(**kwargs):
    pass