import os
import requests
from asana.util import get_value_in_data_file
from furl import furl

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
        self.workspace = get_value_in_data_file('workspace', 'gid')
        self.assignee = get_value_in_data_file('user', 'gid')

    def get_user_info(self):
        """
        Gets the current user of Asana's API.
        return dict: eg: {'gid': str, 'email': [users email]. 'name': [users first and last name]}
        """
        r = self._get('users/me')
        return r.json()['data']

    def get_user_workspaces(self):
        """
        Gets all workspaces visible to authorized user
        return [dict]: eg: {'gid': str, 'name': [name of workspace], 'resource_type': 'workspace'}
        """
        r = self._get('workspaces')
        return r.json()['data']

    def get_projects(self):
        """
        Gets all projects visible to authorized user
        return [dict]: eg: {'gid': str, 'name': [name of project], 'resource_type': 'project'}
        """
        r = self._get('projects')
        return r.json()['data']

    def get_tasks(self, workspace, **params):
        """
        Gets all tasks assigned to authorized user
        return [dict]: eg: {'gid': str, 'name': [name of task], 'resource_type': 'task'}
        """
        r = self._get(f'workspaces/{workspace}/tasks/search', **params)
        return r.json()['data']

    def get_project_tasks(self, project_gid):
        """
        Gets all tasks assigned to authorized user in given project
        return [dict]: eg: [{'gid': str, 'name': [name of task], 'resource_type': 'task'},]
        """
        r = self._get(f'projects/{project_gid}/tasks')
        return r.json()['data']

    def get_project_sections(self, project_gid):
        r = self._get(f'projects/{project_gid}/sections')
        return r.json()['data']

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

    def get_tasks_from_section(self, section_gid):
        """
        Gets all tasks from a given section
        :param section_gid: section id to get tasks in
        :return:
        """
        r = self._get(f'sections/{section_gid}/tasks')
        return r.json()['data']

    def add_task_to_section(self, section_gid, **kwargs):
        """
        Adds a task on the board in the specific section
        :param task_name: name of task
        :param section_gid: section id to add task in
        """
        r = self._post(f'/sections/{section_gid}/addTask', data=kwargs)
        return r.json()['data']

    def _get(self, endpoint: str, data: dict = None, **params):

        url = f'{self.url}/{endpoint}'
        if params:
            params = self.__manipulate_kwargs(params)
            url = self.__with_parameters(url, params)

        r = requests.get(
            url=url,
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

    @staticmethod
    def __with_parameters(url, params):
        unfurled = furl(url)
        unfurled.add(query_params=params)
        return unfurled.url

    @staticmethod
    def __manipulate_kwargs(kwargs):
        if 'assignee' in kwargs.keys():
            kwargs['assignee.any'] = kwargs.pop('assignee')
        if 'sections' in kwargs.keys():
            kwargs['sections.any'] = kwargs.pop('sections')
        return kwargs