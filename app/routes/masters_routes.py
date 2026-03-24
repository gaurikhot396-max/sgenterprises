from flask import Blueprint, render_template
from flask_login import login_required

from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models.enquiry_source import EnquirySource
from app.models.location import Location
from flask import request, redirect, url_for, render_template
from flask_login import login_required
from app.models.enquirystatus import EnquiryStatus
from app.models.followup_result import FollowupResult
from app import db
#from app.routes import masters_bp

#@masters_bp.route("/enquiry-status", methods=["GET", "POST"])
@login_required
def enquiry_status():

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        is_closed = True if request.form.get("is_closed") == "on" else False
        status = "Active" if request.form.get("status") == "on" else "Inactive"
        sort_order = request.form.get("sort_order")

        slug = name.lower().replace(" ", "-")

        new_status = EnquiryStatus(
            name=name,
            slug=slug,
            description=description,
            is_closed=is_closed,
            status=status,
            sort_order=sort_order
        )

        db.session.add(new_status)
        db.session.commit()

        return redirect(url_for("masters.enquiry_status"))

    statuses = EnquiryStatus.query.all()
    return render_template("masters/enquiry_status.html", statuses=statuses)

masters_bp = Blueprint("masters", __name__, url_prefix="/masters")

@masters_bp.route("/enquiry-sources", methods=["GET", "POST"])
def enquiry_sources():

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        status = request.form.get("status")
        sort_order = request.form.get("sort_order")

        new_source = EnquirySource(
            name=name,
            description=description,
            status=status,
            sort_order=sort_order
        )

        db.session.add(new_source)
        db.session.commit()

        return redirect(url_for("masters.enquiry_sources"))

    sources = EnquirySource.query.all()
    return render_template("masters/enquiry_sources.html", sources=sources)

@masters_bp.route("/add-area", methods=["GET", "POST"])
@login_required
def add_area():

    if request.method == "POST":
        city = request.form.get("city")
        area = request.form.get("area")
        description = request.form.get("description")
        status = "Active" if request.form.get("status") == "on" else "Inactive"
        sort_order = request.form.get("sort_order")

        new_area = Location(
            city=city,
            area=area,
            description=description,
            status=status,
            sort_order=sort_order
        )

        db.session.add(new_area)
        db.session.commit()

        return redirect(url_for("masters.add_area"))

    areas = Location.query.all()
    return render_template("masters/add_area.html", areas=areas)


@masters_bp.route("/enquiry-status", methods=["GET", "POST"])
@login_required
def enquiry_status():

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        is_closed = True if request.form.get("is_closed") == "on" else False
        status = "Active" if request.form.get("status") == "on" else "Inactive"
        sort_order = request.form.get("sort_order")

        slug = name.lower().replace(" ", "-")

        new_status = EnquiryStatus(
            name=name,
            slug=slug,
            description=description,
            is_closed=is_closed,
            status=status,
            sort_order=sort_order
        )

        db.session.add(new_status)
        db.session.commit()

        return redirect(url_for("masters.enquiry_status"))

    statuses = EnquiryStatus.query.all()
    return render_template("masters/enquiry_status.html", statuses=statuses)

@masters_bp.route("/followup-result", methods=["GET","POST"])
@login_required
def followup_result():

    if request.method == "POST":

        name = request.form.get("name")
        description = request.form.get("description")
        status = "Active" if request.form.get("status") == "on" else "Inactive"
        sort_order = request.form.get("sort_order")

        new_result = FollowupResult(
            name=name,
            description=description,
            status=status,
            sort_order=sort_order
        )

        db.session.add(new_result)
        db.session.commit()

        return redirect(url_for("masters.followup_result"))

    results = FollowupResult.query.all()

    return render_template(
        "masters/followup_result.html",
        results=results
    )

@masters_bp.route("/setting", methods=["GET","POST"])
@login_required
def setting():

    if request.method == "POST":

        max_followups = request.form.get("max_followups")
        reminder_hours = request.form.get("reminder_hours")
        overdue_alert = True if request.form.get("overdue_alert") else False

        print(max_followups, reminder_hours, overdue_alert)

    return render_template("masters/setting.html")