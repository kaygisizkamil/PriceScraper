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
from service.transform_data_service import process_data


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
                await process_data(hb_data, db)
                await process_data(n11_data, db)
                await process_data(vatan_data, db)

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

async def scheduler(app, db, database_uri):
    while True:
        with app.app_context():
            await fetch_and_process_data(app, db, database_uri)
        await asyncio.sleep(60)