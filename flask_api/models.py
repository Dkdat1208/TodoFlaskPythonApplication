from  flask_api import  db, login_manager
from  flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True , nullable=False)
    username = db.Column(db.String(20), unique=True , nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    status = db.Column(db.Boolean)

    def __repr__(self):
        return f"User('{self.username}')"
