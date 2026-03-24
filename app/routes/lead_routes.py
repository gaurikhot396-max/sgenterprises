from flask import Blueprint, render_template

lead_bp = Blueprint("lead", __name__)


# ---------------- Lead List Page ----------------

@lead_bp.route("/leads")
def lead_list():
    return render_template("leads.html")


# ---------------- Add Lead Page ----------------

@lead_bp.route("/lead/add")
def add_lead():
    return render_template("add_lead.html")