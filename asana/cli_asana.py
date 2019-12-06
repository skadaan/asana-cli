import click
import sys

# all_colors = 'black', 'red', 'green', 'yellow', 'blue', 'magenta', \
#              'cyan', 'white', 'bright_black', 'bright_red', \
#              'bright_green', 'bright_yellow', 'bright_blue', \
#              'bright_magenta', 'bright_cyan', 'bright_white'

from asana.projects import Projects
from asana.workspaces import Workspaces
from asana.tasks import Tasks
from asana.user_account import UserAccount
from asana.util import *


@click.group()
def main():
    if file_exists is False or 'user' not in section_in_data_file():
        me = UserAccount()
        add_to_data_file('user', name=me.account_info.name, gid=me.account_info.gid)
        click.echo(click.style(f'Hello {me.account_info.name} :) Thanks for using asana_cli\n', fg='green'))


@main.command(name='set_default_workspace')
@click.option('--name', required=True)
def set_workspace(name):
    workspaces = Workspaces()
    workspace = workspaces.find_workspace(name)
    if 'workspace' in section_in_data_file():
        current_workspace = get_value_in_data_file('workspace', 'name')
        update_data_file('workspace', gid=workspace.gid, name=workspace.name)
        click.echo(click.style(f'replacing {current_workspace} with {workspace.name} as the default workspace', fg='yellow'))
    else:
        add_to_data_file('workspace', gid=workspace.gid, name=workspace.name)
        click.echo(click.style(f'"{workspace.name}" added as the default project', fg='green'))


@main.command(name='set_default_project')
@click.option('--name', required=True)
def set_default_project(name):
    projects = Projects()
    project = projects.find_project(name)
    board = __get_project_board(project)
    if 'project' in section_in_data_file():
        current_project = get_value_in_data_file('project', 'name')
        update_data_file('project', gid=project.gid, name=project.name, board=str(board))
        click.echo(click.style(f'replacing {current_project} with {project.name} as the default project', fg='yellow'))
    else:
        add_to_data_file('project', gid=project.gid, name=project.name, board=str(board))
        click.echo(click.style(f'"{project.name}" added as the default project', fg='green'))


@main.group(name='show')
def show_():
    pass


@show_.command(name='tasks')
@click.option('--project')
def show_tasks(project=None):
    tasks = Tasks()
    if project is None:
        if file_exists is False or 'project' not in section_in_data_file():
            click.echo(click.style(
                'Project name not provided. Either set a default Project name with the option "set_default_project '
                '--name=<project_name>" or pass in "--project=<project_name>" argument ',
                fg='red'))
            sys.exit(0)
        else:
            project = get_value_in_data_file('project', 'name')
            if get_value_in_data_file('project', 'board') != 'None':
                sections = convert_to_dict(get_value_in_data_file('project', 'board'))
                click.echo(click.style(f'{project} Tasks:', fg='magenta', bold=True, underline=True))
                for section in sections:
                    __section_tasks(tasks, section['gid'], section['name'])
            else:
                tasks.project_gid = get_value_in_data_file('project', 'gid')
                __simple_tasks(tasks)
    else:
        projects = Projects()
        project = projects.find_project(project)

        click.echo(click.style(f'{project.name} Tasks:', bold=True, fg='magenta', underline=True))
        if project.board:
            for section in project.board:
                __section_tasks(tasks, section.gid, section.name)
        else:
            tasks.project_gid = project.gid
            __simple_tasks(tasks)


def __get_project_board(project: Projects):
    if project.board:
        board = ''
        for lane in project.board:
            board += '{"gid": "'+lane.gid+'", "name": "'+lane.name+'"},'
        return board.rstrip(',')


def __simple_tasks(tasks_instance: Tasks):
    tasks = tasks_instance
    tasks = tasks.project_tasks
    __echo_tasks(tasks)


def __section_tasks(tasks_instance: Tasks, section_gid, section_name):
    tasks = tasks_instance
    tasks.section_gid = section_gid
    section_tasks = tasks.project_tasks
    click.echo(click.style(f'\t{section_name}:', fg='white', bold=True))
    if section_tasks:
        __echo_tasks(section_tasks)
    else:
        click.echo(click.style(f'\t(no tasks)', fg='white'))
    print('\n')


def __echo_tasks(tasks):
    for task in tasks:
        status = 'done' if task.completed else 'incomplete'
        color = 'yellow' if status == 'incomplete' else 'blue'
        click.echo(click.style(f'\t- {task.name}', fg=color))


if __name__ == '__main__':
    main()
