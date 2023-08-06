import aiohttp
import asyncpg
from dateutil import parser
from model.hepsiburda_datas import HepsiburadaData
from model.data_from_different_sources import From_different_sources


async def process_data(data, db):
    # Process the fetched data here and perform database operations
    for notebook in data:
        # Extract the required attributes from the notebook data
        product_name = notebook["product_name"]
        product_link = notebook["product_link"]
        saved_time_str = notebook["saved_time"]
        saved_time = parser.parse(saved_time_str)

        # Create a new From_different_sources object
        notebook_data = From_different_sources(
            product_name=product_name,
            product_link=product_link,
            saved_time=saved_time
        )

        # Add the new object to the session
        db.session.add(notebook_data)

    # Commit the changes to the database
    db.session.commit()

async def fetch_data_from_hepsiburda_source(session: aiohttp.ClientSession, page_number: int) -> list:
    url = f'http://localhost:5000/api/hepsiburda/notebooks/getall?page={page_number}'

    try:
        async with session.get(url) as response:
            data = await response.json()
            return data
    except aiohttp.ClientError as e:
        print(f"An error occurred while fetching data from source, page {page_number}: {e}")
        return []


async def fetch_data_from_vatan_source(session: aiohttp.ClientSession, page_number: int) -> list:
    url = f'http://localhost:5000/api/vatan/notebooks/getall?page={page_number}'

    try:
        async with session.get(url) as response:
            data = await response.json()
            return data
    except aiohttp.ClientError as e:
        print(f"An error occurred while fetching data from source, page {page_number}: {e}")
        return []


async def fetch_data_from_n11_source(session: aiohttp.ClientSession, page_number: int) -> list:
    url = f'http://localhost:5000/api/n11/notebooks/getall?page={page_number}'

    try:
        async with session.get(url) as response:
            data = await response.json()
            return data
    except aiohttp.ClientError as e:
        print(f"An error occurred while fetching data from source, page {page_number}: {e}")
        return []

