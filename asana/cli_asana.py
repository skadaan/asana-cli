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


@click.group()
def main():
    # me = UserAccount()
    # click.echo(click.style(f'Hello {me.account_info.name}. Thanks for using asana_cli', fg='green'))
    pass


@main.command(name='set_default_project')
@click.option('--project', required=True)
def set_default_project(project):
    projects = Projects()
    project = projects.find_project(project)
    data = {'default_project': {'gid': project.gid, 'name': project.name}}
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
                'Project name not provided. Either set a default Project name with "set_default_project '
                '--project=<project_name>" or pass in "--project=<project_name>" argument ',
                fg='red'))
            sys.exit(0)
        else:
            project = data['default_project']['name']
            tasks.project_gid = data['default_project']['gid']
    else:
        projects = Projects()
        tasks.project_gid = projects.find_project(project).gid
    tasks = tasks.project_tasks
    click.echo(click.style(f'{project} tasks:', bold=True))

    for task in tasks:
        status = 'done' if task.completed else 'incomplete'
        color = 'bright_magenta' if status == 'incomplete' else 'cyan'
        click.echo(
            click.style(f'\t{task.name}', fg=color))


if __name__ == '__main__':
    main()
