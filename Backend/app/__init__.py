import os
from flask import Flask, make_response
from app.extensions import db, cors
from app.config import config


def create_app():
    app = Flask(__name__)

    # Load config
    env = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[env])

    # ── Create database folder BEFORE anything else touches the DB ──
    db_folder = os.path.join(os.path.dirname(__file__), '..', 'database')
    db_folder = os.path.abspath(db_folder)
    os.makedirs(db_folder, exist_ok=True)

    # ── Override DB URI to use the absolute path ──
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(db_folder, 'db.sqlite3')}"

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Handle OPTIONS preflight for all routes
    @app.after_request
    def add_cors(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
        return response

    @app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
    @app.route('/<path:path>', methods=['OPTIONS'])
    def options_handler(path):
        return make_response('', 204)

    # Register blueprints
    from app.routes.events  import events_bp
    from app.routes.counts  import counts_bp
    from app.routes.reports import reports_bp

    app.register_blueprint(events_bp)
    app.register_blueprint(counts_bp)
    app.register_blueprint(reports_bp)

    # Import models so SQLAlchemy sees them
    from app.models.event import Event

    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully")
        print(f"✅ Database location: {os.path.join(db_folder, 'db.sqlite3')}")

    # Health check
    @app.route('/')
    def health():
        return {'status': 'ok', 'message': 'CCTV Monitoring API is running'}

    return app