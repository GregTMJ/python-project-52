import json
import os


FILES = {
    'users': 'users.json',
    'status': 'status.json',
    'labels': 'labels.json',
    'tasks': 'tasks.json',
    'task_users': 'task_users.json',
    'task_labels': 'task_labels.json',
}


def get_fixture_path(file_name: str):
    """
    Combines path with fixtures and needed file
    :return: a combined dirname
    """
    workdir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(workdir, 'fixtures', file_name)


def read_json(file_name: str):
    """
    Reads data from json files inside fixtures
    :return: loaded data
    """
    json_file = get_fixture_path(file_name)
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def get_data(category) -> dict | None:
    """
    In testing we give what category we are testing, and depending
    on what we are looking, we search for it in the correct json
    file
    :return: data from fixtures category json file
    """
    look_file = FILES.get(category, None)
    if look_file:
        return read_json(look_file)
