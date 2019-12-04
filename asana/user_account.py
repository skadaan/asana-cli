from asana.api import AsanaAPI
from asana.asna_resources_type import User


class UserAccount(AsanaAPI):

    def __init__(self):
        super().__init__()
        self.account_info = self.user_details

    @property
    def user_details(self) -> User:
        r = self.get_user_info()
        return User(
            gid=r['gid'],
            email=r['email'],
            name=r['name'],
            )
