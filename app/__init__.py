from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

menu = [{"name": "List all tasks", "url": "/tasks"},
        {"name": "Create a task","url": "/tasks/post"},
        {"name": "View one task", "url": f"/tasks/task_id"},
        {"name": "Update task", "url": f"/tasks/update"},
        {"name": "Delete task", "url": f"/tasks/delete"},
        {"name": "Mark complete","url": f"/tasks/{id}/mark_complete"},
        {"name": "Mark incomplete","url": f"/tasks/{id}/mark_incomplete"},
        {"name": "Main page","url": "about"}]

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    #secret key is required to send flash messages
    app.secret_key =os.environ.get("SECRET_KEY")



    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.task import Task
    from app.models.goal import Goal

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)

    from .routes.goals import goals_bp
    app.register_blueprint(goals_bp)

    @app.errorhandler(404)
    def pageNotFound(error):
        return render_template('page404.html', title='page not found', menu=menu), 404 

    @app.route("/base")
    @app.route("/about")
    def about():
        print(url_for('about'))
        return render_template('about.html', title="The Task List Project by: Nina Patrina. Ada Developers Academy, 2022", menu=menu)   
    
    return app
