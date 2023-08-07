import asyncio
import flask
from model.dbmodel import db
import asyncio
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
import asyncio
import aiohttp
import aiopg
from model.data_from_different_sources import From_different_sources
import asyncpg
import datetime
from dateutil import parser
from service. transform_data_service import fetch_data_from_hepsiburda_source
from service. transform_data_service import fetch_data_from_n11_source

from service. transform_data_service import fetch_data_from_vatan_source

import asyncio
import aiohttp
from datetime import datetime, timedelta
import aiocron
from model.hepsiburda_datas import HepsiburadaData

from service.transform_data_service import  fetch_and_parse_product_data


async def fetch_and_process_data(app, db, database_uri):
    
    async with aiohttp.ClientSession() as session:
        hb_page = 1
        n11_page = 1
        vatan_page = 1

        hb_has_data = True
        n11_has_data = True
        vatan_has_data = True

        while hb_has_data or n11_has_data or vatan_has_data:
            hb_data = await fetch_data_from_hepsiburda_source(session, hb_page)
            n11_data = await fetch_data_from_n11_source(session, n11_page)
            vatan_data = await fetch_data_from_vatan_source(session, vatan_page)

            # Check if all data lists are empty
            if len(hb_data) == 0:
                hb_has_data = False
            if len(n11_data) == 0:
                n11_has_data = False
            if len(vatan_data) == 0:
                vatan_has_data = False

            with app.app_context():
                #await process_data(hb_data, db)
                #await process_data(n11_data, db)
                await process_data(session,vatan_data, database_uri,db,app)

            if hb_has_data:
                hb_page += 1
            if n11_has_data:
                n11_page += 1
            if vatan_has_data:
                vatan_page += 1
  
    print("Number of requests made by each service:")
    print("Hepsiburada:", hb_page - 1)
    print("N11:", n11_page - 1)
    print("Vatan:", vatan_page - 1)    
    
async def process_data(session,data, database_uri,db,app):
    with app.app_context():  # Set up the Flask application context within the background thread

        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db.create_engine(database_uri)))

        for notebook in data:   
            product_data_from=await fetch_and_parse_product_data(session,notebook["product_link"])   
            if product_data_from:   
                product_name = notebook["product_name"] 
                product_link = notebook["product_link"]     
                fromWhere=notebook["fromWhere"]
                image_link=notebook['image_link']
                saved_time_str = notebook["saved_time"]    
                saved_time = parser.parse(saved_time_str)                    
                cpu=product_data_from['cpu']    
                ram=product_data_from['ram']      
                screen=product_data_from['screen']    
                gpu=product_data_from['gpu']  
                os=product_data_from['os']       
                ssd=product_data_from['ssd']       
                hdd=product_data_from['hdd']            
                notebook_data = From_different_sources(
                    product_name=product_name,
                    product_link=product_link,
                    image_link=image_link,
                    fromWhere=fromWhere,
                    saved_time=saved_time,
                    cpu=cpu,
                    ram=ram,
                    screen=screen,
                    gpu=gpu,
                    os=os,
                    ssd=ssd,
                    hdd=hdd
                )   
                
            else:       
                continue           
                        
            db.session.add(notebook_data)             

        db.session.commit()    

async def scheduler(app, db, database_uri):
    while True:
        with app.app_context():
            await fetch_and_process_data(app, db, database_uri)
        await asyncio.sleep(60)