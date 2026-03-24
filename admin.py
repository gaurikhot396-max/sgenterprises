from app import create_app
from app.extensions import db, bcrypt
from app.models.user import User

app = create_app()

with app.app_context():

    existing_user = User.query.filter_by(username="admin").first()

    if not existing_user:

        hashed_password = bcrypt.generate_password_hash("admin123").decode("utf-8")

        admin = User(
            username="admin",
            password=hashed_password,
            role="Admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("✅ Admin Created Successfully!")

    else:
        print("⚠ Admin Already Exists!")