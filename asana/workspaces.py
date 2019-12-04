from asana.api import AsanaAPI
from asana.asna_resources_type import WorkspaceResource


class Workspaces(AsanaAPI):

    @property
    def get_workpaces(self) -> [WorkspaceResource]:
        workspaces = []
        r = self.get_user_workspaces()
        for i, workspace in enumerate(r):
            workspaces.append(WorkspaceResource(
                index=i,
                gid=workspace['gid'],
                name=workspace['name'],
                resource_type=workspace['resource_type']))
        return workspaces

    def find_workspace(self, workspace_name):
        workspaces = self.get_workpaces
        workspace = [workspace for workspace in workspaces if workspace_name.lower() in workspace.name.lower()]
        if workspace:
            return workspace.pop()
        raise ValueError(f'Cannot find {workspace_name}')
