class WorkspaceResource:
    def __init__(self, gid, name, resource_type, index):
        self.index = index
        self.gid = gid
        self.name = name
        self.resource_type = resource_type


class User:
    def __init__(self, gid, email, name):
        self.gid = gid
        self.email = email
        self.name = name


class SectionResource:
    def __init__(self, index, gid, name, resource_type, tasks=None):
        self.index = index
        self.gid = gid
        self.name = name
        self.resource_type = resource_type
        if tasks:
            self.tasks: [TaskResource] = tasks


class ProjectResource:
    def __init__(self, gid, name, resource_type, index, board=None):
        self.index = index
        self.gid = gid
        self.name = name
        self.resource_type = resource_type
        self.board = board


class TaskResource:
    def __init__(self, gid, name, resource_type, index, assignee=None, completed=None):
        self.index = index
        self.gid = gid
        self.name = name
        self.assignee = assignee
        self.completed = completed
        self.resource_type = resource_type
