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
# from asana.cli.echo_entry import entry_
from cli.echo_set_default import EchoSetDefault, __echo_set_verbiage, __echo_replace_verbiage

SECTION_ID = None
SECTION_GID = None
SECTION_NAME = None

TASK_ID = -1
TASK_GID = None
TASK_NAME = None

list_of_tasks = list()


@click.group()
def main():
    pass
    # if file_exists is False or 'user' not in section_in_data_file():
    #     me = UserAccount()
    #     add_to_data_file('user', name=me.account_info.name, gid=me.account_info.gid)
    #     click.echo(click.style(f'Hello {me.account_info.name} :) Thanks for using asana_cli\n', fg='green'))


__set = EchoSetDefault()


@main.group(name='set')
def set_():
    pass


@set_.command(name='workspace')
@click.option('--name', required=True)
def set_workspace(name):
    __set.set_workspace(name)
    click.echo(click.style(
        __echo_set_verbiage(__set.workspace) if not __set.prev_workspace else
        __echo_replace_verbiage(__set.prev_workspace, __set.workspace),
        fg=__set.echo_color
    ))


@set_.command(name='project')
@click.option('--name', required=True)
def set_workspace(name):
    __set.set_project(name)
    click.echo(click.style(
        __echo_set_verbiage(__set.project) if not __set.prev_project else
        __echo_replace_verbiage(__set.prev_project, __set.project),
        fg=__set.echo_color
    ))


@main.group(name='show')
def show_():
    pass


@show_.command(name='tasks')
@click.option('--project')
def show_tasks(project=None):

    tasks = Tasks()
    if project is None:
        if file_exists() is False or 'project' not in section_in_data_file():
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
                global SECTION_NAME, SECTION_GID, SECTION_ID
                for i, section in enumerate(sections):
                    SECTION_ID = i
                    SECTION_GID = section['gid']
                    SECTION_NAME = section['name']
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
    add_to_task_file(list_of_tasks)


@main.group(name='move', chain=True)
def move_():
    pass


@move_.command(name='task')
@click.option('--task_id')
@click.option('--name')
def show_tasks(task_id=None, name=None):
    click.echo(f'{task_id}')


@move_.command(name='to')
@click.option('--section_id')
@click.option('--name')
def show_tasks(section_id=None, name=None):
    click.echo(f'{section_id}')


# def __get_project_board(project: Projects):
#     if project.board:
#         board = ''
#         for lane in project.board:
#             board += '{"gid": "'+lane.gid+'", "name": "'+lane.name+'"},'
#         return board.rstrip(',')


def __simple_tasks(tasks_instance: Tasks):
    tasks = tasks_instance
    tasks = tasks.project_tasks
    __echo_tasks(tasks)


def __section_tasks(tasks_instance: Tasks, section_gid, section_name):
    tasks = tasks_instance
    tasks.section_gid = section_gid
    section_tasks = tasks.project_tasks
    click.echo(click.style(f'(S{SECTION_ID}) \t{section_name}:', fg='white', bold=True))
    list_of_tasks.append({
        'section_id': f'S{SECTION_ID}',
        'section_gid': SECTION_GID,
        'section_name': SECTION_NAME,
        'tasks': []
    })
    if section_tasks:
        __echo_tasks(section_tasks)

    else:
        click.echo(click.style(f'\t(no tasks)', fg='white'))
    print('\n')


def __echo_tasks(tasks):
    global TASK_GID, TASK_ID, TASK_NAME
    for i, task in enumerate(tasks):
        TASK_ID += 1
        TASK_GID = task.gid
        TASK_NAME = task.name
        status = 'done' if task.completed else 'incomplete'
        color = 'yellow' if status == 'incomplete' else 'blue'
        click.echo(click.style(f'\t- (T{TASK_ID}) {task.name}', fg=color))
        index = [i for i, section in enumerate(list_of_tasks) if section['section_gid'] == SECTION_GID]
        list_of_tasks[index.pop()]['tasks'].append({
            'task_id': f'T{TASK_ID}',
            'task_gid': TASK_GID,
            'task_name': TASK_NAME
        })


if __name__ == '__main__':
    main()
