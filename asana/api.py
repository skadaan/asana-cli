import os
import sys
import json
import requests
from urllib.error import HTTPError

try:
    ASANA_TOKEN = os.environ['ASANA_TOKEN']
except:
    raise KeyError("Please set ASANA_TOKEN as an environment variable.")

URL = 'https://app.asana.com/api/1.0'
HEADERS = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {ASANA_TOKEN}'}


class AsanaAPI:
    def __init__(self):
        self.url = URL
        self.headers = HEADERS

    def get_user_info(self):
        """
        Gets the current user of Asana's API. 
        return dict: eg: {'gid': str, 'email': [users email]. 'name': [users first and last name]}
        """
        r = self._get('users/me')
        return r.json()

    def get_user_workspaces(self):
        """
        Gets all workspaces visible to authorized user
        return [dict]: eg: {'gid': str, 'name': [name of workspace], 'resource_type': 'workspace'}
        """
        r = self._get('workspaces')
        return r.json()

    def get_projects(self):
        """
        Gets all projects visible to authorized user
        return [dict]: eg: {'gid': str, 'name': [name of project], 'resource_type': 'project'}
        """
        r = self._get('projects')
        return r.json()

    def get_tasks(self):
        """
        Gets all tasks assigned to authorized user
        return [dict]: eg: {'gid': str, 'name': [name of task], 'resource_type': 'task'}
        """
        r = self._get('tasks')
        return r.json()

    def get_project_tasks(self, project_gid):
        """
        Gets all tasks assigned to authorized user in given project
        return [dict]: eg: [{'gid': str, 'name': [name of task], 'resource_type': 'task'},]
        """
        r = self._get(f'projects/{project_gid}/tasks')
        return r.json()

    def get_project_sections(self, project_gid):
        r = self._get(f'projects/{project_gid}/sections')
        return r.json()

    def get_tasks_details(self, task_gid):
        """
        Gets additial detils on each task. ie: assignee, completed, etc.
        """
        r = self._get(f'tasks/{task_gid}')
        return r.json()['data']

    def update_task(self, task_gid, **kwargs):
        """
        Updates the given task from task_gid
        """
        r = self._put(f'tasks/{task_gid}', data=kwargs)
        return r.json()['data']

    def _get(self, endpoint: str, data: dict = None):
        r = requests.get(
            url=f'{self.url}/{endpoint}',
            headers=self.headers,
            data=data)
        if int(r.status_code) == 200 or int(r.status_code) == 201:
            return r
        # raise HTTPError(f'{r.status_code}: {r.content}')

    def _post(self, endpoint: str, data: dict):
        r = requests.post(
            url=f'{self.url}/{endpoint}',
            headers=HEADERS,
            data=data)
        if int(r.status_code) == 200 or int(r.status_code) == 201:
            return r
        # raise HTTPError(f'{r.status_code}: {r.content}')

    def _put(self, endpoint: str, data: dict):
        r = requests.put(
            url=f'{self.url}/{endpoint}',
            headers=HEADERS,
            data=data)
        if int(r.status_code) == 200 or int(r.status_code) == 201:
            return r
        # raise HTTPError(f'{r.status_code}: {r.content}')