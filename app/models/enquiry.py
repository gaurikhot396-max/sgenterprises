from app.extensions import db
from datetime import datetime
from app.models.user import User

from app.extensions import db
from datetime import datetime
from app.models.user import User

class Enquiry(db.Model):
    __tablename__ = "enquiries"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    customer = db.Column(db.String(100))
    mobile = db.Column(db.String(15))
    alt_mobile = db.Column(db.String(15))
    email = db.Column(db.String(100))
    source = db.Column(db.String(50))
    area = db.Column(db.String(100))
    city = db.Column(db.String(100))
    product = db.Column(db.String(100))
    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id"))
    status = db.Column(db.String(50))       # Open, Followup, Closed
    closed = db.Column(db.String(50)) 

    # Assigned To
    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    assigned_user = db.relationship(
        "User",
        foreign_keys=[assigned_to],
        back_populates="assigned_enquiries"
    )

    # Created By
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_user = db.relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_enquiries"
    )

    status = db.Column(db.String(50), default="Open")
    closed = db.Column(db.String(20))
    
    remark = db.Column(db.Text)
    followup_date=db.Column(db.Date, nullable=True)
    followups = db.relationship("FollowUp", backref="enquiry", lazy=True)