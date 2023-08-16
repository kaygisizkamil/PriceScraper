import asyncio
import flask
from service.transform_data_service import fetch_and_parse_product_data_hb
from service.transform_data_service import fetch_data_from_hb_source
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
import requests

from service. transform_data_service import fetch_data_from_vatan_source

import asyncio
import aiohttp
from datetime import datetime, timedelta
import aiocron
from model.hepsiburda_datas import HepsiburadaData

from service.transform_data_service import  fetch_and_parse_product_data_vatan
from sqlalchemy.orm import sessionmaker

async def process_data(all_results, database_uri, db, app):

    with app.app_context():
        start = time.time()

        
        print(f"Data fetch completed in {time.time() - start} seconds")
        print(all_results)

        notebook_data_list = []
        for specs in all_results:
            notebook_data = From_different_sources(
                review_count=specs['review_count'],
                review_rating=specs['review_rating'],
                price=specs['price'],
                brand_name=specs["brand_name"],
                product_name=specs["product_name"],
                product_link=specs["product_link"],
                image_link=specs['image_link'],
                fromWhere=specs["fromWhere"],
                cpu=specs['cpu'],
                ram=specs['ram'],
                screen=specs['screen'],
                gpu=specs['gpu'],
                os=specs['os'],
                ssd=specs['ssd'],
                hdd=specs['hdd']
            )
            notebook_data_list.append(notebook_data)

        Session = sessionmaker(autocommit=False, autoflush=False, bind=db.create_engine(database_uri))
        with Session.begin() as db_session:
            db_session.add_all(notebook_data_list)
            db_session.commit()
        print(f"Data fetch completed in {time.time() - start} seconds")
async def scheduler(app, db, database_uri):
    while True:
        start = time.time()
          
        print("Starting data fetch...")
        
        async with aiohttp.ClientSession() as session:
            vatan_page = 1
            hepsiburda_page = 1
            n11_page = 1
            
            vatan_has_data = True
            hepsiburda_has_data = True
            n11_has_data = False
            
            while vatan_has_data or hepsiburda_has_data or n11_has_data:
                vatan_data = await fetch_data_from_vatan_source(session, vatan_page)
                #print("VATANDAN DATA ALINDI")
                
                hepsiburda_data = await fetch_data_from_hb_source(session, hepsiburda_page)
                print("HEPSIBURADA DATA ALINDI")

                #n11_data = await fetch_data_from_n11_source(session, n11_page)
                #print("N11 DATA ALINDI")

                vatan_has_data = bool(vatan_data)
                hepsiburda_has_data = bool(hepsiburda_data)
                #n11_has_data = bool(n11_data)


                try:
                    vatan_results = await fetch_and_parse_product_data_vatan(session, vatan_data)
                except Exception as e:
                    print(f"An error occurred while fetching and parsing Vatan data: {e}")
                    vatan_results = None

                try:
                    hepsiburda_results = await fetch_and_parse_product_data_hb(session, hepsiburda_data)
                except Exception as e:
                    print(f"An error occurred while fetching and parsing Hepsiburada data: {e}")
                    hepsiburda_results = None

                '''   try:
                    n11_results = await fetch_and_parse_product_data_n11(session, n11_data)
                except Exception as e:
                    print(f"An error occurred while fetching and parsing N11 data: {e}")
                    n11_results = []
                    '''
                all_results = []

                if hepsiburda_results is not None:
                    all_results.extend(hepsiburda_results)

                if vatan_results is not None:
                    all_results.extend(vatan_results)

                # Process data only if there are results for the respective source
                if all_results:
                    await process_data(all_results, database_uri, db, app)

                if vatan_has_data:
                    vatan_page += 1
                if hepsiburda_has_data:
                    hepsiburda_page += 1
                if n11_has_data:
                    n11_page += 1

            print(f"Data fetch completed in {time.time() - start} seconds")
            print("Number of requests made by each service:")
            print("Vatan:", vatan_page - 1)
            print("Hepsiburda:", hepsiburda_page - 1)
            print("N11:", n11_page - 1)
            
        await asyncio.sleep(2400)  # Run again every 4 minutes
