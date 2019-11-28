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


class Section:
    def __init__(self, gid, name, resource_type):
        self.gid = gid
        self.name = name
        self.resource_type = resource_type


class ProjectResource:
    def __init__(self, gid, name, resource_type, index, board=None):
        self.index = index
        self.gid = gid
        self.name = name
        self.resource_type = resource_type
        if board:
            self.board: [Section] = board


class TaskResource:
    def __init__(self, gid, name, assignee, completed, resource_type, index):
        self.index = index
        self.gid = gid
        self.name = name
        self.assignee = assignee
        self.completed = completed
        self.resource_type = resource_type
