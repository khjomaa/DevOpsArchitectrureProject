from app import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User


class User(UserMixin):

    def __init__(self, user_json):
        self.user_json = user_json

    def get_id(self):
        object_id = self.user_json.get('id')
        return object_id
