from app import db

class EnquiryStatus(db.Model):
    __tablename__ = "enquiry_status"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_closed = db.Column(db.Boolean, default=False)   # checkbox Is Closed
    status = db.Column(db.String(20), default="Active")  # Active / Inactive
    sort_order = db.Column(db.Integer, default=1)