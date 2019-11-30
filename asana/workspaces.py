from api import AsanaAPI
from asna_resources_type import WorkspaceResource


class Workspaces(AsanaAPI):

    def get_workpaces(self) -> [WorkspaceResource]:
        workspaces = []
        r = r.json()
        for i, workspace in enumerate(r['workspaces']):
            workspaces.append(WorkspaceResource(
                index=i,
                gid=workspace['gid'],
                name=workspace['name'],
                resource_type=workspace['resource_type']))
        return workspaces
