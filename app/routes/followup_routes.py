from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models.followup import FollowUp
from app.models.enquiry import Enquiry
from datetime import datetime, date

followup_bp = Blueprint("followup", __name__, url_prefix="/followup")

# Route to display all follow-ups
@followup_bp.route("/all")
@login_required
def all_followups():

    query = FollowUp.query.join(Enquiry)

    status = request.args.get("status")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    assigned_to = request.args.get("assigned_to")

    today = date.today()

    # 🔥 STATUS FILTER
    if status == "Due Today":
        query = query.filter(FollowUp.followup_date == today)

    elif status == "Overdue":
        query = query.filter(FollowUp.followup_date < today)

    elif status == "Completed":
        query = query.filter(FollowUp.status == "Completed")

    elif status == "Pending":
        query = query.filter(FollowUp.status == "Pending")

    # 🔥 DATE FILTER
    if date_from:
        query = query.filter(FollowUp.followup_date >= date_from)

    if date_to:
        query = query.filter(FollowUp.followup_date <= date_to)

    # 🔥 ASSIGNED FILTER
    if assigned_to:
        query = query.filter(FollowUp.assigned_to == assigned_to)

    followups = query.order_by(FollowUp.followup_date.desc()).all()

    enquiries = Enquiry.query.all()

    return render_template(
        "followup/all_followups.html",
        followups=followups,
        enquiries=enquiries
    )


# Route to add a new follow-up
@followup_bp.route("/add", methods=["POST"])
@login_required
def add_followup():

    try:
        followup = FollowUp(
            enquiry_id=request.form.get("enquiry_id"),
            followup_date=datetime.strptime(request.form.get("followup_date"), "%Y-%m-%d"),
            followup_time=datetime.strptime(request.form.get("followup_time"), "%H:%M").time() if request.form.get("followup_time") else None,
            followup_type=request.form.get("followup_type"),
            remark=request.form.get("remark"),
            assigned_to="Admin"  # later dynamic करू शकतो
        )

        db.session.add(followup)
        db.session.commit()

        flash("Follow-up added successfully!", "success")

    except Exception as e:
        db.session.rollback()
        flash(str(e), "danger")

    return redirect(url_for("followup.all_followups"))