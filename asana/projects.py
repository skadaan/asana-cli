from api import AsanaAPI
from asna_resources_type import ProjectResource

from asna_resources_type import Section


class Projects(AsanaAPI):

    def __init__(self):
        super().__init__()

    @property
    def projects(self):
        projects = []
        r = self.get_projects()
        for i, project in enumerate(r['data']):
            sections = self.get_project_sections(project['gid'])
            if 'no section' not in sections['data'].pop()['name']:
                sections = []
                for section in sections:
                    sections.append(Section(
                        gid=section['gid'],
                        name=section['name'],
                        resource_type=section['resource_type']
                    ))
            else:
                sections = None
            projects.append(ProjectResource(
                index=i,
                gid=project['gid'],
                name=project['name'],
                resource_type=project['resource_type'],
                board=sections
            ))
        return projects

    def find_project(self, project_name):
        projects = self.projects
        project = [project for project in projects if project_name.lower() in project.name.lower()]
        if project:
            return project.pop()
        raise ValueError(f'Cannot find {project_name}')