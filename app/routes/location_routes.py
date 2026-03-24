from flask import Blueprint, jsonify
from app.models.location import Location

location_bp = Blueprint("location", __name__)

@location_bp.route("/locations")
def get_locations():

    locations = Location.query.filter_by(status=True).all()

    data = []

    for loc in locations:
        data.append({
            "id": loc.id,
            "city": f"{loc.city}, {loc.district}, {loc.state}"
        })

    return jsonify(data)