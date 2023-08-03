import asyncio
import threading
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import Blueprint, jsonify  # Import other necessary modules
from model.dbmodel import db
from model.hepsiburda_datas import HepsiburadaData 
from model.vatandatas import VatanData
from model.n11_datas import N11Data
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test@localhost:5432/FinalProject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# No need to initialize the databases again
# hepsiburda_db.init_app(app)
# vatan_db.init_app(app)
#db = SQLAlchemy()
db.init_app(app)

async def start_tasks(database_uri):
    from controller.hepsiburda_notebook_controller import hepsiburada_blueprint
   # from scheduler.hepsiburda_notebook_scheduler import schedule_task_for_hepsiburada
    from controller.vatan_notebook_controller import vatan_blueprint
    from scheduler.vatan_notebook_scheduler import schedule_task_for_vatan
    from scheduler.n11_notebook_scheduler import schedule_task_for_n11
    #from controller.vatan_notebook_controller import vatan_blueprint

    app.register_blueprint(hepsiburada_blueprint, url_prefix='/api/hepsiburda')
    app.register_blueprint(vatan_blueprint,url_prefix='/api/vatan')
    #app.register_blueprint(vatan_blueprint, url_prefix='/api/vatan')

    # Get the current event loop (Flask's event loop)
    loop = asyncio.get_event_loop()

    # Run the scheduler for the Hepsiburada notebook in the current event loop
    n11_task=asyncio.create_task(schedule_task_for_n11(app,db,database_uri))
   # hepsiburada_task = asyncio.create_task(schedule_task_for_hepsiburada(app,db,database_uri))  # Pass the database URI as a parameter
    vatan_task = asyncio.create_task(schedule_task_for_vatan(app,db, database_uri))
    
    # Run the scheduler in the current event loop
    #await hepsiburada_task
    await vatan_task
    await n11_task
if __name__ == "__main__":
    # Create the database tables based on the models
    with app.app_context():
        db.create_all()

    server_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    server_thread.start()
    try:
        # Run the async tasks in the event loop
        asyncio.run(start_tasks(app.config['SQLALCHEMY_DATABASE_URI']))  # Pass the database URI as a parameter        
        server_thread.join()

    except KeyboardInterrupt:
        print("Interrupted.")
        print("Exiting.")