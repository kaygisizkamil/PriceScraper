from service.vatan_notebook_service import get_product_data
from model.vatandatas import VatanData
import asyncio
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
import asyncio
import aiohttp
import asyncpg
from dateutil import parser




initial_data_extraction_complete = False
data_extraction_lock = asyncio.Lock()
async def schedule_task_for_vatan(app, db,database_uri):
    global initial_data_extraction_complete

    while True:  # Run the loop indefinitely for periodic scheduling
        with app.app_context():  # Set up the Flask application context within the background thread
            try:
                print("Notebook Scheduler started.")
                for page_number in range(1, 15):
                    product_data = await get_product_data(page_number)  # Await the async function here
                    if not product_data:
                        # Continue to the next page if no reasonable product data is found
                        continue

                    # Save the product data to the database
                    async with data_extraction_lock:
                        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db.create_engine(database_uri)))
                        for single_product in product_data:
                            product_data_entry = VatanData(
                                product_name=single_product['product_name'],
                                brand_name=single_product['brand_name'],
                                price=single_product['price'],
                                review_rating=single_product['review_rating'],
                                review_count=single_product['review_count'],
                                product_link=single_product['product_link'],
                                image_link=single_product['image_link']
                            )
                            session.add(product_data_entry)

                        session.commit()
                        session.remove()

                        print(f"Data from URL: https://www.vatanbilgisayar.com/notebook/?page={page_number} saved to the database.")

                # Mark initial data extraction as complete after the first iteration is done
                if not initial_data_extraction_complete:
                    initial_data_extraction_complete = True

            except KeyboardInterrupt:
                print("Notebook Scheduler interrupted.")

            # Sleep for the specified interval (60 seconds)
            await asyncio.sleep(240)