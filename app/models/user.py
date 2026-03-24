from app.extensions import db
from flask_login import UserMixin

from app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="Admin")

    # Relationships
    assigned_enquiries = db.relationship(
        "Enquiry",
        foreign_keys="Enquiry.assigned_to",
        back_populates="assigned_user"
    )

    created_enquiries = db.relationship(
        "Enquiry",
        foreign_keys="Enquiry.created_by",
        back_populates="created_user"
    )

    def __repr__(self):
        return f"<User {self.username}>"