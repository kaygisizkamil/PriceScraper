import asyncio
import threading
import sched
import time
from flask import Flask
from model.vatandatas import db
from controller.vatan_notebook_controller import vatan_blueprint
from scheduler.vatan_notebook_scheduler import schedule_task_for_notebook

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test@localhost:5432/FinalProject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Register the blueprint
app.register_blueprint(vatan_blueprint)

# Initialize and configure the database
db.init_app(app)

if __name__ == "__main__":
    # Create the database tables based on the models
    with app.app_context():
        db.create_all()

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=app.run)
    flask_thread.start()

    # Start the scheduler for the notebook in a separate thread
    s = sched.scheduler(time.time, time.sleep)  # Create the sched.scheduler object
    notebook_scheduler_thread = threading.Thread(target=lambda: asyncio.run(schedule_task_for_notebook(s, app, 'postgresql://postgres:test@localhost:5432/FinalProject')))  # Use asyncio.run to run the async function
    notebook_scheduler_thread.start()

    try:
        # Keep the main thread running to allow the Flask server and the scheduler to execute
        while flask_thread.is_alive() or notebook_scheduler_thread.is_alive():
            flask_thread.join(1)
            notebook_scheduler_thread.join(1)

    except KeyboardInterrupt:
        print("Interrupted.")
        print("Exiting.")