import click
import json
import sys
from os import path

# all_colors = 'black', 'red', 'green', 'yellow', 'blue', 'magenta', \
#              'cyan', 'white', 'bright_black', 'bright_red', \
#              'bright_green', 'bright_yellow', 'bright_blue', \
#              'bright_magenta', 'bright_cyan', 'bright_white'
from projects import Projects
from tasks import Tasks
from user_account import UserAccount


@click.group()
def main():
    me = UserAccount()
    click.echo(click.style(f'Hello {me.account_info.name} :) Thanks for using asana_cli', fg='green'))


@main.command(name='set_default_project')
@click.option('--project', required=True)
def set_default_project(project):
    projects = Projects()
    project = projects.find_project(project)
    data = {'default_project': {'gid': int(project.gid), 'name': project.name}}
    if project.board:
        data['default_project']['board'] = []
        for board in project.board:
            data['default_project']['board'].append({'gid': int(board.gid), 'name': board.name})
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)
    click.echo(click.style(f'"{project.name}" added as the default project', fg='green'))


@main.group(name='show')
def show_():
    pass


@show_.command(name='tasks')
@click.option('--project')
def show_tasks(project=None):
    tasks = Tasks()
    if project is None:
        file_exists = path.exists("data.json")
        if file_exists:
            with open('data.json') as f:
                data = f.read()
                if data:
                    data = json.loads(data)
        if file_exists is False or len(data) == 0 or 'default_project' not in data.keys():
            click.echo(click.style(
                'Project name not provided. Either set a default Project name with the option "set_default_project '
                '--project=<project_name>" or pass in "--project=<project_name>" argument ',
                fg='red'))
            sys.exit(0)
        else:
            project = data['default_project']['name']
            if 'board' in data['default_project'].keys():
                sections = data['default_project']['board']
                click.echo(click.style(f'{project} Tasks:', fg='magenta', bold=True, underline=True))
                for section in sections:
                    __section_tasks(tasks, section['gid'], section['name'])
            else:
                tasks.project_gid = data['default_project']['gid']
                __simple_tasks(tasks)
    else:
        projects = Projects()
        project = projects.find_project(project)

        click.echo(click.style(f'{project.name} Tasks:', bold=True, fg='magenta', underline=True))
        if project.board:
            for section in project.board:
                __section_tasks(tasks, section.gid, section.name)
        else:
            __simple_tasks(tasks)


def __simple_tasks(tasks_instance: Tasks):
    tasks = tasks_instance
    tasks = tasks.project_tasks
    for task in tasks:
        status = 'done' if task.completed else 'incomplete'
        color = 'yellow' if status == 'incomplete' else 'blue'
        click.echo(click.style(f'\t- {task.name}', fg=color))


def __section_tasks(tasks_instance: Tasks, section_gid, section_name):
    tasks = tasks_instance
    tasks.section_gid = section_gid
    section_tasks = tasks.project_tasks
    click.echo(click.style(f'\t{section_name}:', fg='white', bold=True))
    if section_tasks:
        for task in section_tasks:
            status = 'done' if task.completed else 'incomplete'
            color = 'yellow' if status == 'incomplete' else 'blue'
            click.echo(click.style(f'\t- {task.name}', fg=color))
    else:
        click.echo(click.style(f'\t(no tasks)', fg='white'))
    print('\n')


if __name__ == '__main__':
    main()
