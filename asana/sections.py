from asana.api import AsanaAPI


class Sections(AsanaAPI):

    def __init__(self, section_gid=None, section_name=None):
        self.section_gid = section_gid
        self.section_name = section_name

    def tasks_in_section(self):
        r = self.get_tasks_from_section(self.section_gid)