from app import db

class Location(db.Model):

    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100))
    city = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(db.String(10), default="Active")
    sort_order = db.Column(db.Integer)