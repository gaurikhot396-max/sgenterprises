from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.enquiry import Enquiry
from app.extensions import db
from datetime import date   # ✅ ADD THIS
from sqlalchemy import func
from datetime import timedelta
from sqlalchemy import and_

dashboard_bp = Blueprint("dashboard", __name__)

# Common Stats Function
def get_stats(user_id=None):

    today = date.today()

    query = Enquiry.query

    # ⭐ Particular user filter
    if user_id:
        query = query.filter(Enquiry.assigned_to == user_id)

    stats = {}

    stats["date_count"] = Enquiry.query.filter(
        Enquiry.date == today
    ).count()

    stats["month_count"] = Enquiry.query.filter(
        db.extract("month", Enquiry.date) == today.month,
        db.extract("year", Enquiry.date) == today.year
    ).count()

    stats["interested"] = Enquiry.query.filter(
        Enquiry.closed == "Interested"
    ).count()

    stats["not_interested"] = Enquiry.query.filter(
        Enquiry.closed == "Not Interested"
    ).count()

    stats["won"] = Enquiry.query.filter(
        Enquiry.closed == "Won"
    ).count()

    stats["lost"] = Enquiry.query.filter(
        Enquiry.closed == "Lost"
    ).count()

    stats["open"] = Enquiry.query.filter(
        Enquiry.closed == None
    ).count()

    stats["due_today"] = 0
    stats["overdue"] = 0

    # Enquiries Today
    stats["date_count"] = query.filter(Enquiry.date == today).count()

    # Enquiries This Month
    stats["month_count"] = query.filter(
        db.extract("month", Enquiry.date) == today.month,
        db.extract("year", Enquiry.date) == today.year
    ).count()

    # Follow-ups
    stats["due_today"] = query.filter(Enquiry.followup_date == today).count()
    stats["overdue"] = query.filter(Enquiry.followup_date < today, Enquiry.status != "Closed").count()

    # Open / Interested / Not Interested
    stats["open"] = query.filter(Enquiry.status == "Open").count()
    stats["interested"] = query.filter(Enquiry.closed == "Interested").count()
    stats["not_interested"] = query.filter(Enquiry.closed == "Not Interested").count()

    # Closing ratio
    stats["won"] = query.filter(Enquiry.closed == "Won").count()
    stats["lost"] = query.filter(Enquiry.closed == "Lost").count()

    return stats


# ---------------- Admin Dashboard ----------------
@dashboard_bp.route("/admin/dashboard")
@login_required
def admin_dashboard():

    if current_user.role != "Admin":
        return "Access Denied"

    stats = get_stats(current_user.id)

    return render_template("dashboard.html", stats=stats)


# ---------------- Executive Dashboard ----------------
@dashboard_bp.route("/executive/dashboard")
@login_required
def executive_dashboard():

    if current_user.role != "Executive":
        return "Access Denied"

    stats = get_stats()

    return render_template("dashboard.html", stats=stats)


# ---------------- Manager Dashboard ----------------
@dashboard_bp.route("/manager/dashboard")
@login_required
def manager_dashboard():

    if current_user.role != "Manager":
        return "Access Denied"

    stats = get_stats()

    return render_template("dashboard.html", stats=stats)