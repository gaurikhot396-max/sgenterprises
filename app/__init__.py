from flask import Flask, redirect, url_for
from config import Config
from app.extensions import db, login_manager, bcrypt


def create_app():

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Redirect to login page if user not logged in
    login_manager.login_view = "index"

    # Import blueprints
    from app.routes.index_routes import index_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.lead_routes import lead_bp
    from app.routes.enquiry_routes import enquiry_bp
    from app.routes.location_routes import location_bp
    from app.routes.followup_routes import followup_bp
    from app.routes.masters_routes import masters_bp
    from app.routes.reports_routes import reports_bp
    from app.routes.users_routes import users_bp
    

    # Register blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(lead_bp)
    app.register_blueprint(enquiry_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(followup_bp)
    app.register_blueprint(masters_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(users_bp)

    # Default route → open login page
    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
