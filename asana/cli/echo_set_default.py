from asana.projects import Projects, get_project_board
from asana.user_account import UserAccount
from asana.util import *
from asana.workspaces import Workspaces


class EchoSetDefault:

    def __init__(self):
        self.me = None
        self.prev_workspace = None
        self.workspace = self.__workspace
        self.prev_project = None
        self.project = self.__project
        self.echo_color = 'yellow' if self.prev_workspace else 'green'

    @property
    def __workspace(self):
        if 'workspace' in section_in_data_file():
            return get_value_in_data_file('workspace', 'name')

    @property
    def __project(self):
        if 'project' in section_in_data_file():
            return get_value_in_data_file('project', 'name')

    def is_new_user(self):
        if file_exists() is False or 'user' not in section_in_data_file():
            self.me = UserAccount()
        else:
            return False

    def set_workspace(self, name):
        workspaces = Workspaces()
        workspace = workspaces.find_workspace(name)
        if self.workspace:
            self.prev_workspace = self.workspace
            update_data_file('workspace', gid=workspace.gid, name=workspace.name)
        else:
            add_to_data_file('workspace', gid=workspace.gid, name=workspace.name)
        self.workspace = workspace.name

    def set_project(self, name):
        projects = Projects()
        project = projects.find_project(name)
        board = get_project_board(project)
        if self.project:
            self.prev_project = self.project
            update_data_file('project', gid=project.gid, name=project.name, board=str(board))
        else:
            add_to_data_file('project', gid=project.gid, name=project.name, board=str(board))
        self.project = project.name


def __echo_set_verbiage(new):
    return f'"{new}" added as the default project'


def __echo_replace_verbiage(prev, new):
    return f'replacing "{prev}" with "{new}" as the default workspace'
