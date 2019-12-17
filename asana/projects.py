from asana.api import AsanaAPI
from asana.asna_resources_type import ProjectResource, SectionResource


class Projects(AsanaAPI):

    def __init__(self):
        super().__init__()

    @property
    def projects(self):
        projects = []
        r = self.get_projects()
        for i, project in enumerate(r):
            sections = None
            projects.append(ProjectResource(
                index=i,
                gid=project['gid'],
                name=project['name'],
                resource_type=project['resource_type'],
                board=sections))
        return projects

    def find_project(self, project_name):
        projects = self.projects
        project = [project for project in projects if project_name.lower() in project.name.lower()].pop()
        r = self.get_project_sections(project.gid)
        if 'no section' not in r[0]['name']:
            sections = []
            for j, section in enumerate(r):
                sections.append(SectionResource(
                    index=j,
                    gid=section['gid'],
                    name=section['name'],
                    resource_type=section['resource_type']))
            project.board = sections
        if project:
            return project
        raise ValueError(f'Cannot find {project_name}')


def get_project_board(project: Projects):
    if project.board:
        board = ''
        for lane in project.board:
            board += '{"gid": "'+lane.gid+'", "name": "'+lane.name+'"},'
        return board.rstrip(',')