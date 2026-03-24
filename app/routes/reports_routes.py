from flask import Blueprint, render_template
from flask_login import login_required
from flask import request, send_file
from io import BytesIO
import pandas as pd
from app.extensions import db 
from app.models.enquiry import Enquiry
from weasyprint import HTML
from sqlalchemy import func, case
from flask import jsonify
from io import BytesIO, StringIO
import csv
from app.models.followup import FollowUp


reports_bp = Blueprint("reports", __name__, url_prefix="/reports")

@reports_bp.route("/areawise-report", methods=["GET"])
@login_required
def areawise_report():
    # Filters
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    area = request.args.get("area")

    # Base query
    query = Enquiry.query

    if date_from:
        query = query.filter(Enquiry.date >= date_from)
    if date_to:
        query = query.filter(Enquiry.date <= date_to)
    if area and area != "All Areas":
        query = query.filter(Enquiry.area == area)

    enquiries = query.order_by(Enquiry.date.desc()).all()

    # Export CSV
    if request.args.get("export") == "csv":
        data = [{
            "Date": e.date.strftime('%d-%m-%Y') if e.date else "",
            "Customer": e.customer,
            "Mobile": e.mobile,
            "Source": e.source,
            "Area": e.area,
            "Assigned To": e.assigned_user.username if e.assigned_user else "",
            "Status": e.status
        } for e in enquiries]

        df = pd.DataFrame(data)
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        return send_file(
            output,
            as_attachment=True,
            download_name="areawise_enquiries.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Export PDF
    if request.args.get("export") == "pdf":
        rendered = render_template("reports/areawise_report.html", enquiries=enquiries)
        pdf_file = BytesIO()
        HTML(string=rendered).write_pdf(pdf_file)
        pdf_file.seek(0)
        return send_file(
            pdf_file,
            as_attachment=True,
            download_name="areawise_enquiries.pdf",
            mimetype="application/pdf"
        )

    # Normal HTML render
    return render_template("reports/areawise_report.html", enquiries=enquiries)

@reports_bp.route("/closing-nonclosingRe")
@login_required
def closing_nonclosingRe():
    return render_template("reports/closing_nonclosingRe.html")

@reports_bp.route("/datawise-report", methods=["GET"])
@login_required
def datawise_report():
    # 1️⃣ Get filter values from query params
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    # 2️⃣ Base query
    query = Enquiry.query

    if date_from:
        query = query.filter(Enquiry.date >= date_from)
    if date_to:
        query = query.filter(Enquiry.date <= date_to)

    enquiries = query.order_by(Enquiry.date.desc()).all()

    # 3️⃣ Export CSV if requested
    if request.args.get("export") == "csv":
        data = [{
            "Date": e.date.strftime('%d-%m-%Y') if e.date else "",
            "Customer": e.customer,
            "Mobile": e.mobile,
            "Source": e.source,
            "Area": e.area,
            "Assigned To": e.assigned_user.username if e.assigned_user else "",
            "Status": e.status,
            "Closed": "Yes" if e.closed else "No"
        } for e in enquiries]

        df = pd.DataFrame(data)
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        return send_file(output,as_attachment=True,download_name="enquiries.xlsx",mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # 4️⃣ Export PDF if requested
    if request.args.get("export") == "pdf":
        rendered = render_template("reports/datawise_report.html", enquiries=enquiries)
        pdf_file = BytesIO()
        HTML(string=rendered).write_pdf(pdf_file)
        pdf_file.seek(0)
        return send_file(
    pdf_file,
    as_attachment=True,download_name="enquiries.pdf",mimetype="application/pdf")

    # 5️⃣ Normal HTML render
    return render_template("reports/datawise_report.html", enquiries=enquiries)

@reports_bp.route("/followup-effect")
@login_required
def followup_effect():
    return render_template("reports/followup_effect.html")

@reports_bp.route("/sourcewise-report", methods=["GET"])
@login_required
def sourcewise_report():
    sources = db.session.query(Enquiry.source).distinct().all()

    # Filters
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    source = request.args.get("source")

    # Base Query
    query = Enquiry.query

    if date_from:
        query = query.filter(Enquiry.date >= date_from)

    if date_to:
        query = query.filter(Enquiry.date <= date_to)

    if source and source != "All Sources":
        query = query.filter(Enquiry.source == source)

    enquiries = query.order_by(Enquiry.date.desc()).all()

    # =========================
    # CSV / Excel Export
    # =========================
    if request.args.get("export") == "csv":

        data = []

        for e in enquiries:
            data.append({
                "Date": e.date.strftime('%d-%b-%Y') if e.date else '',
                "Customer": e.customer,
                "Mobile": e.mobile,
                "Source": e.source,
                "Area": e.area,
                "Assigned To": e.assigned_user.username if e.assigned_user else "",
                "Status": e.status
            })

        df = pd.DataFrame(data)

        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="sourcewise_report.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # =========================
    # PRINT / PDF
    # =========================
    if request.args.get("export") == "pdf":
        return render_template(
            "reports/sourcewise_report.html",
            enquiries=enquiries,
            print_mode=True
        )

    # =========================
    # Normal Page
    # =========================
    return render_template(
        "reports/sourcewise_report.html",
        enquiries=enquiries,
        sources=[s[0] for s in sources]
    )

@reports_bp.route("/sales-executive")
@login_required
def sales_executive():

    results = (
        db.session.query(
            Enquiry.assigned_to.label("sales_executive"),
            func.count(Enquiry.id).label("total_enquiries"),
            func.sum(case((Enquiry.closed == "Won", 1), else_=0)).label("closed_won"),
            func.sum(case((Enquiry.closed == "Lost", 1), else_=0)).label("closed_lost"),
        )
        .group_by(Enquiry.assigned_to)
        .all()
    )

    report_data = []
    chart_labels = []
    chart_won = []
    chart_lost = []

    for r in results:
        conversion = (r.closed_won / r.total_enquiries * 100) if r.total_enquiries else 0

        report_data.append({
            "sales_executive": r.sales_executive,
            "total_enquiries": r.total_enquiries,
            "closed_won": r.closed_won,
            "closed_lost": r.closed_lost,
            "conversion": round(conversion, 2)
        })

        chart_labels.append(r.sales_executive)
        chart_won.append(r.closed_won)
        chart_lost.append(r.closed_lost)

    # ✅ PDF Export
    if request.args.get("export") == "pdf":

        rendered = render_template(
            "reports/sales_executive.html",
            report_data=report_data
        )

        pdf_file = BytesIO()

        HTML(string=rendered).write_pdf(pdf_file)

        pdf_file.seek(0)

        return send_file(
            pdf_file,
            as_attachment=True,
            download_name="sales_executive_report.pdf",
            mimetype="application/pdf"
        )

    return render_template(
        "reports/sales_executive.html",
        report_data=report_data,
        chart_labels=chart_labels,
        chart_won=chart_won,
        chart_lost=chart_lost
    )

@reports_bp.route("/closing-nonclosing")
@login_required
def closing_nonclosing():

    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    closing_type = request.args.get("closing_type")

    query = Enquiry.query

    if date_from:
        query = query.filter(Enquiry.date >= date_from)

    if date_to:
        query = query.filter(Enquiry.date <= date_to)

    if closing_type == "Closing":
        query = query.filter(Enquiry.closed == "Won")

    elif closing_type == "Non-Closing":
        query = query.filter(Enquiry.closed == "Lost")

    enquiries = query.all()

    # ---------------- CSV EXPORT ----------------
    if request.args.get("export") == "csv":

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow([
        e.date.strftime('%d-%m-%Y') if e.date else "",
        e.customer,
        e.source,
        e.assigned_user.username if e.assigned_user else "",
        e.closed,
        e.remark
        ])

        for e in enquiries:
            writer.writerow([
                e.date,
                e.customer,
                e.source,
                e.assigned_to,
                e.closed,
                e.remark
            ])

        output.seek(0)

        return send_file(
            BytesIO(output.getvalue().encode()),
            as_attachment=True,
            download_name="closing_nonclosing_report.csv",
            mimetype="text/csv"
        )

    # ---------------- PDF EXPORT ----------------
    if request.args.get("export") == "pdf":

        rendered = render_template(
            "reports/closing_nonclosing.html",
            enquiries=enquiries
        )

        pdf_file = BytesIO()
        HTML(string=rendered).write_pdf(pdf_file)
        pdf_file.seek(0)

        return send_file(
            pdf_file,
            as_attachment=True,
            download_name="closing_nonclosing_report.pdf",
            mimetype="application/pdf"
        )

    return render_template(
        "reports/closing_nonclosing.html",
        enquiries=enquiries
    )

@reports_bp.route("/followup-result")
@login_required
def followup_result():

    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    # ---------------- BASE QUERY ----------------
    query = db.session.query(FollowUp, Enquiry).join(
        Enquiry, FollowUp.enquiry_id == Enquiry.id
    )

    if date_from:
        query = query.filter(FollowUp.followup_date >= date_from)

    if date_to:
        query = query.filter(FollowUp.followup_date <= date_to)

    results = query.order_by(FollowUp.followup_date.desc()).all()

    # ---------------- CSV EXPORT ----------------
    if request.args.get("export") == "csv":

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "Followup No",
            "Followup Date",
            "Enquiry ID",
            "Customer",
            "Result",
            "Completed",
            "Remark"
        ])

        for f, e in results:
            writer.writerow([
                f.id,
                f.followup_date.strftime('%d-%m-%Y') if f.followup_date else "",
                e.id,
                e.customer,
                f.result,
                f.completed,
                f.remark
            ])

        output.seek(0)

        return send_file(
            BytesIO(output.getvalue().encode()),
            as_attachment=True,
            download_name="followup_report.csv",
            mimetype="text/csv"
        )

    # ---------------- PDF EXPORT ----------------
    if request.args.get("export") == "pdf":

        rendered = render_template(
            "reports/followup_effect.html",
            results=results
        )

        pdf_file = BytesIO()
        HTML(string=rendered).write_pdf(pdf_file)
        pdf_file.seek(0)

        return send_file(
            pdf_file,
            as_attachment=True,
            download_name="followup_report.pdf",
            mimetype="application/pdf"
        )

    # ---------------- NORMAL PAGE ----------------
    return render_template(
        "reports/followup_effect.html",
        results=results
    )

