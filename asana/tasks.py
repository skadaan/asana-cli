from asana.api import AsanaAPI
from asana.asna_resources_type import TaskResource
from asana.util import get_value_in_data_file


class Tasks(AsanaAPI):

    def __init__(self, workspace_gid=None, project_gid=None, section_gid=None):
        super().__init__()
        self.workspace_gid = workspace_gid
        self.project_gid = project_gid
        self.section_gid = section_gid

    @property
    def project_tasks(self) -> [TaskResource]:
        r = self.get_tasks(workspace=self.workspace, assignee=self.assignee, sections=self.section_gid, completed=False)
        if len(r) == 0:
            return
        tasks = []
        for i, task in enumerate(r):
            tasks.append(TaskResource(
                index=i,
                gid=task['gid'],
                name=task['name'],
                resource_type=task['resource_type']))
        return tasks

    def update_task_complete_status(self, task_name, completion: bool):
        r = self.__get_tasks
        task = [task for task in r if task_name.lower() in task.name.lower()]
        if task:
            task_to_update = task.pop()
            self.update_task(task_to_update.gid, completion)
        raise ValueError(f'No task found with name {task_name}')

    @property
    def __get_tasks(self):
        if self.workspace_gid:
            pass
        if self.project_gid:
            return self.get_project_tasks(self.project_gid)
        if self.section_gid:
            return self.get_tasks_from_section(self.section_gid)
        return self.get_tasks()
