import asyncio
import threading
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import Blueprint, jsonify 
from model.dbmodel import db
from model.hepsiburda_datas import HepsiburadaData 
from model.vatandatas import VatanData
from model.n11_datas import N11Data
from model.data_from_different_sources import From_different_sources
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": ["https://price-scraper-frontend-static.onrender.com","https://price-scraper-irdo.onrender.com"]}}, supports_credentials=True)

db_username = "admin"
db_password = "80s7caMIowdQutwg7MxwBmaRnIPJ86ri"
db_host = "dpg-cjfvl8k1ja0c73e36sr0-a.oregon-postgres.render.com"
db_port = 5432
db_name = "final_project_f04r"

# Construct the database URI
db_uri = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:fZb9iIc0DLPb6Fcypy5oNWTTF9C9Uy5d@dpg-cjhc2ob6fquc73b4p7cg-a/final_project_5twh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#Database'i baslat singleton baglanti modeliyle diger servicelerin ayni instance-baglantiyi kullanmasini sagla

db.init_app(app)
with app.app_context():
        db.create_all()
async def start_tasks(database_uri):
    from scheduler.hepsiburda_notebook_scheduler import schedule_task_for_hepsiburada
    from scheduler.vatan_notebook_scheduler import schedule_task_for_vatan
    from scheduler.n11_notebook_scheduler import schedule_task_for_n11
    from scheduler.transform_data_scheduler import   scheduler
    

    

    # Flask event loopunu al
    loop = asyncio.get_event_loop()
    #Background taski ekle
   # n11_task=asyncio.create_task(schedule_task_for_n11(app,db,database_uri))
    hepsiburada_task = asyncio.create_task(schedule_task_for_hepsiburada(app,db,database_uri))  # Database uri'ini parametre olarak gecir
    vatan_task = asyncio.create_task(schedule_task_for_vatan(app,db, database_uri))
    transform_task=asyncio.create_task(scheduler(app,db, database_uri))

    #async await mantigi ile bir gorevin calismasinin digerini etkilememesi icin await ile gorevleri cagir
    #await transform_task
    await transform_task 
 
    await hepsiburada_task
    
    await vatan_task
    #await n11_task

if __name__ == "__main__":
    from controller.n11_notebook_controller import n11_blueprint
    from controller.vatan_notebook_controller import vatan_blueprint
    from controller.hepsiburda_notebook_controller import hepsiburada_blueprint
    from controller.aggregated_data_controller import all_brands_blueprint,all_processors_blueprint,all_rams_blueprint,all_screen_sizes_blueprint,all_cheapest_computers_blueprint,all_price_range_blueprint,all_sidebar_computers_blueprint,all_matched_computers_blueprint
   
    

    app.register_blueprint(hepsiburada_blueprint, url_prefix='/api/hepsiburda')
    app.register_blueprint(vatan_blueprint,url_prefix='/api/vatan')
    app.register_blueprint(n11_blueprint,url_prefix='/api/n11')
    app.register_blueprint(all_brands_blueprint,url_prefix='/api/aggregated')
    app.register_blueprint(all_processors_blueprint,url_prefix='/api/aggregated')
    app.register_blueprint(all_rams_blueprint,url_prefix='/api/aggregated')
    app.register_blueprint(all_screen_sizes_blueprint,url_prefix='/api/aggregated')
    app.register_blueprint(all_cheapest_computers_blueprint,url_prefix='/api/aggregated')
    app.register_blueprint(all_price_range_blueprint,url_prefix='/api/aggregated')
    app.register_blueprint(all_sidebar_computers_blueprint,url_prefix='/api/aggregated')    #maybe we gotta make this in another base api,
    app.register_blueprint(all_matched_computers_blueprint,url_prefix='/api/aggregated')    #maybe we gotta make this in another base api,
   #serveri ayri bir threadde calisir
    server_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 10000})
    server_thread.start()
    try:
        #flask background tasklerini diger bir threadde calistir
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_tasks(app.config['SQLALCHEMY_DATABASE_URI']))
        server_thread.join()    

    except KeyboardInterrupt:
        print("Interrupted.")
        print("Exiting.")
        
        