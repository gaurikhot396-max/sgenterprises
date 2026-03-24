from app import db

class FollowupResult(db.Model):

    __tablename__ = "followup_result"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    status = db.Column(db.String(20))
    sort_order = db.Column(db.Integer)