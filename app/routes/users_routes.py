from flask import Blueprint, render_template
from flask_login import login_required
from app.models.user import User

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/all-users")
@login_required
def all_users():

    users = User.query.all()

    return render_template(
        "users/all_users.html",
        users=users
    )


@users_bp.route("/roles-permission")
@login_required
def roles_permission():

    roles = [
        {"id":1,"role_name":"Admin","permissions_count":24,"user_count":1},
        {"id":2,"role_name":"Manager","permissions_count":11,"user_count":1},
        {"id":3,"role_name":"Sales Executive","permissions_count":5,"user_count":1}
    ]

    return render_template(
        "users/roles_permission.html",
        roles=roles
    )
from app.extensions import db, bcrypt
from app.models.user import User
from flask import request, redirect, url_for, flash


@users_bp.route("/add-user", methods=["POST"])
@login_required
def add_user():

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    role = request.form.get("role")

    if password != confirm_password:
        flash("Passwords do not match")
        return redirect(url_for("users.all_users"))

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    flash("User added successfully")

    return redirect(url_for("users.all_users"))