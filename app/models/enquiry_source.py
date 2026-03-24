from app.extensions import db

class EnquirySource(db.Model):
    __tablename__ = "enquiry_sources"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(db.String(20))
    sort_order = db.Column(db.Integer)
    