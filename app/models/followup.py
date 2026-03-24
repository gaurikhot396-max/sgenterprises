from app.extensions import db
from datetime import datetime

class FollowUp(db.Model):
    __tablename__ = "followups"

    id = db.Column(db.Integer, primary_key=True)
    enquiry_id = db.Column(db.Integer, db.ForeignKey("enquiries.id"))

    followup_date = db.Column(db.Date)
    followup_time = db.Column(db.Time)
    followup_type = db.Column(db.String(50))  # Call / Meeting / Demo
    remark = db.Column(db.Text)
    status = db.Column(db.String(50), default="Pending")  # Pending / Completed

    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id"))
    result_id = db.Column(db.Integer, db.ForeignKey("followup_result.id"))
    result = db.relationship("FollowupResult", backref="followups")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    