from projects import Projects
from util import file_exists, section_in_data_file, get_value_in_data_file, convert_to_dict


class EchoShowTasks:

    def __init__(self, project=None):
        self.project = project
        self.is_default_project_set: bool = self.__is_default_property_set
        if self.is_default_project_set:
            self.project = get_value_in_data_file('project', 'name')
        else:
            self.project = self.get_project()
        self.sections = None

    @property
    def __is_default_property_set(self):
        if file_exists() and 'project' in section_in_data_file():
            return True
        return False

    @property
    def sections(self):
        return self.sections

    @sections.setter
    def sections(self, value):
        if self.is_default_project_set:
            self.sections = convert_to_dict(get_value_in_data_file('project', 'board'))
        else:
            self.sections = self.project.board

    def get_project(self):
        projects = Projects()
        return projects.find_project(self.project)
