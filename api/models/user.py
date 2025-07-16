from extensions import db
from config.config import Role

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    role = db.Column(db.Enum(Role), nullable=False, default=Role.GUEST)

    def __init__(self, username, role, blocked=False):
        self.username = username
        self.role = role

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role.name
        }