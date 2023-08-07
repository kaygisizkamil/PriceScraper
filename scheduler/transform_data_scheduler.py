import asyncio
import flask
from model.dbmodel import db
import asyncio
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
import asyncio
import aiohttp
import time
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
            #hb_data = await fetch_data_from_hepsiburda_source(session, hb_page)
            #n11_data = await fetch_data_from_n11_source(session, n11_page)
            vatan_data = await fetch_data_from_vatan_source(session, vatan_page)
            print("VATANDAN DATA ALINDI")
            # Check if all data lists are empty
            #if len(hb_data) == 0:
             #   hb_has_data = False
            #if len(n11_data) == 0:
             #   n11_has_data = False
            if len(vatan_data) == 0:
                vatan_has_data = False

            #with app.app_context():
                #await process_data(hb_data, db)
                #await process_data(n11_data, db)
             #   print("enter to vatan parser")

            await process_data(session,vatan_data, database_uri,db,app)
            print("VATAN DATASI PARSE EDILDI")

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
async def process_data(session, data, database_uri, db, app):
    initial_data_extraction_complete = False
    data_extraction_lock = asyncio.Lock()
    with app.app_context():
        async with data_extraction_lock:
            session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db.create_engine(database_uri)))
            start = time.time()

            print("product details:")         
            product_details = await fetch_and_parse_product_data(session, data)
            print(product_details)
            print(f"Data fetch completed in {time.time() - start} seconds")

            for specs in product_details:
                notebook_data = From_different_sources(
                    product_name=specs["product_name"],
                    product_link=specs["product_link"],  
                    image_link=specs['image_link'],
                    fromWhere=specs["fromWhere"], 
                    saved_time=parser.parse(specs["saved_time"]),
                    cpu=specs['cpu'],
                    ram=specs['ram'],     
                    screen=specs['screen'], 
                    gpu=specs['gpu'],      
                    os=specs['os'],          
                    ssd=specs['ssd'],      
                    hdd=specs['hdd']  
                )
                session.add(notebook_data)         

            if not initial_data_extraction_complete:
                initial_data_extraction_complete = True

        session.commit()
                #session.remove()   

async def scheduler(app, db, database_uri):
    while True:
        start = time.time()
          
        print("Starting data fetch...")
      
        await fetch_and_process_data(app, db, database_uri)
        
        print(f"Data fetch completed in {time.time() - start} seconds")
         
        await asyncio.sleep(60)  # Run again every 4 minutes