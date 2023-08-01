import asyncio
import time
import sched
import threading
from flask import Flask
from scheduler.hepsiburda_notebook_scheduler import schedule_task_for_hepsiburada
from scheduler.vatan_notebook_scheduler import schedule_task_for_vatan
from controller.hepsiburda_notebook_controller import hepsiburada_blueprint
from controller.vatan_notebook_controller import vatan_blueprint
from model.vatandatas import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test@localhost:5432/FinalProject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Register the blueprints
app.register_blueprint(vatan_blueprint)
app.register_blueprint(hepsiburada_blueprint)

# Initialize and configure the database
db.init_app(app)

if __name__ == "__main__":
    # Create the database tables based on the models
    with app.app_context():
        db.create_all()

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=app.run)
    flask_thread.start()

    # Start the scheduler for the Vatan notebook in a separate thread
    vatan_scheduler_thread = threading.Thread(target=lambda: asyncio.run(schedule_task_for_vatan(s, app, 'postgresql://postgres:test@localhost:5432/FinalProject')))
    vatan_scheduler_thread.start()

    # Start the scheduler for the Hepsiburada notebook in a separate thread
    hepsiburada_scheduler_thread = threading.Thread(target=lambda: asyncio.run(schedule_task_for_hepsiburada(s, app, 'postgresql://postgres:test@localhost:5432/FinalProject')))
    hepsiburada_scheduler_thread.start()

    try:
        # Keep the main thread running to allow the Flask server and the schedulers to execute
        while flask_thread.is_alive() or vatan_scheduler_thread.is_alive() or hepsiburada_scheduler_thread.is_alive():
            flask_thread.join(1)
            vatan_scheduler_thread.join(1)
            hepsiburada_scheduler_thread.join(1)

    except KeyboardInterrupt:
        print("Interrupted.")
        print("Exiting.")