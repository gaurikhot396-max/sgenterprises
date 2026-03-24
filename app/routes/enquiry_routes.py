# app/routes/enquiry.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required
from app.extensions import db
from app.models.enquiry import Enquiry
from app.models.location import Location
from app.models.user import User  # ✅ Import User from correct file
from datetime import datetime
from werkzeug.security import generate_password_hash
from io import BytesIO
import pandas as pd
import io



import pandas as pd
from flask import send_file
import io

# Blueprint setup
enquiry_bp = Blueprint(
    "enquiry",
    __name__,
    url_prefix="/enquiry"
)

# ------------------------------
# Route: All Enquiries
# ------------------------------
@enquiry_bp.route("/all")
@enquiry_bp.route("/enquiries")
@login_required
def all_enquiries():

    try:
        query = Enquiry.query.order_by(Enquiry.id.desc())

        # GET values
        date_from = request.args.get("date_from")
        date_to = request.args.get("date_to")
        source = request.args.get("source")
        city = request.args.get("city")
        search = request.args.get("search")
        assigned_to = request.args.get("assigned_to")

        # DATE FILTER
        if date_from:
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d").date()
            query = query.filter(Enquiry.date >= date_from_obj)

        if date_to:
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d").date()
            query = query.filter(Enquiry.date <= date_to_obj)

        # SOURCE FILTER
        if source and source != "All Sources":
            query = query.filter(Enquiry.source == source)

        # CITY FILTER
        if city:
            query = query.filter(Enquiry.city == city)
        # ASSIGNED USER FILTER
        if assigned_to:
            query = query.filter(Enquiry.assigned_to == assigned_to)

        # SEARCH FILTER
        if search:
            query = query.filter(
                Enquiry.customer.ilike(f"%{search}%")
            )

        enquiries = query.all()

        # FILTER DROPDOWN DATA
        states = db.session.query(Enquiry.area).distinct().all()
        cities = db.session.query(Enquiry.city).distinct().all()
        users = User.query.all()

    except Exception as e:
        flash(f"Error fetching enquiries: {str(e)}", "danger")
        enquiries = []
        states = []
        cities = []

    return render_template(
        "enquiry/all_enquiries.html",
        enquiries=enquiries,
        states=[s[0] for s in states],
        cities=[c[0] for c in cities],
        users=users
    )

# ------------------------------
# Route: Add Enquiry
# ------------------------------
@enquiry_bp.route("/add-enquiry", methods=["GET", "POST"])
@login_required
def add_enquiry():
    sales_users = User.query.filter_by(role="Sales Executive").all()

    if request.method == "POST":
        try:
            date_obj = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
            new_enquiry = Enquiry(
                date=date_obj,
                customer=request.form.get("customer"),
                mobile=request.form.get("mobile"),
                alt_mobile=request.form.get("alt_mobile"),
                email=request.form.get("email"),
                source=request.form.get("source"),
                area=request.form.get("area"),
                city=request.form.get("city"),
                product=request.form.get("product"),
                assigned_to=int(request.form.get("assigned_to")),
                remark=request.form.get("remark"),
                status=request.form.get("status")
            )
            db.session.add(new_enquiry)
            db.session.commit()
            flash("Enquiry added successfully!", "success")
            return redirect(url_for("enquiry.all_enquiries"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding enquiry: {str(e)}", "danger")

    locations = Location.query.all()
    states = list(set([l.state for l in locations]))
    cities = list(set([l.city for l in locations]))

    return render_template("enquiry/add_enquiry.html",
                           sales_users=sales_users,
                           states=states,
                           cities=cities)

# ------------------------------
# Route: Edit Enquiry
# ------------------------------
@enquiry_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_enquiry(id):
    enquiry = Enquiry.query.get_or_404(id)

    sales_users = User.query.filter_by(role="sales").all()  # ✅ pass to template

    if request.method == "POST":
        try:
            enquiry.date = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
            enquiry.customer = request.form.get("customer")
            enquiry.mobile = request.form.get("mobile")
            enquiry.alt_mobile = request.form.get("alt_mobile")
            enquiry.email = request.form.get("email")
            enquiry.source = request.form.get("source")
            enquiry.area = request.form.get("area")
            enquiry.city = request.form.get("city")
            enquiry.product = request.form.get("product")
            enquiry.assigned_to = int(request.form.get("assigned_to"))  # ✅ FK
            enquiry.status = request.form.get("status") 
            enquiry.remark = request.form.get("remark")

            db.session.commit()
            flash("Enquiry updated successfully!", "success")
            return redirect(url_for("enquiry.all_enquiries"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating enquiry: {str(e)}", "danger")

    return render_template("enquiry/edit_enquiry.html", enquiry=enquiry, sales_users=sales_users)

# ------------------------------
# Route: Delete Enquiry
# ------------------------------
@enquiry_bp.route("/delete/<int:id>")
@login_required
def delete_enquiry(id):
    enquiry = Enquiry.query.get_or_404(id)

    try:
        db.session.delete(enquiry)
        db.session.commit()
        flash("Enquiry deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting enquiry: {str(e)}", "danger")

    return redirect(url_for("enquiry.all_enquiries"))

@enquiry_bp.route("/export-excel")
@login_required
def export_excel():

    enquiries = Enquiry.query.all()

    data = []

    for e in enquiries:
        data.append({
            "Enquiry Date": e.date,
            "Customer Name": e.customer,
            "Mobile Number": e.mobile,
            "Alternate Mobile": e.alt_mobile,
            "Email": e.email,
            "Source of Enquiry": e.source,
            "State": e.area,
            "City": e.city,
            "Product / Service Interested": e.product,
            "Assigned To": e.assigned_user.username if e.assigned_user else "",
            "Initial Remark": e.remark
        })

    df = pd.DataFrame(data)

    output = BytesIO()
    df.to_excel(output, index=False)

    output.seek(0)

    return send_file(
        output,
        download_name="enquiries.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )