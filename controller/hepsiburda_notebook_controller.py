from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from model.hepsiburda_datas import HepsiburadaDataReadOnly


hepsiburada_blueprint = Blueprint('hepsiburada', __name__)

# http://localhost:5000/api/hepsiburda/notebooks/getall?page=5
@hepsiburada_blueprint.route('/notebooks/getall', methods=['GET'])
def hepsiburada_get_all_notebooks():
    # Get the requested page number from the query parameters (default to 1 if not provided)
    page = request.args.get('page', 1, type=int)
    
    # Number of items per page (adjust this value based on your requirements)
    items_per_page = 100

    # Calculate the offset to fetch the data for the requested page
    offset = (page - 1) * items_per_page

    # Get the latest saved time from the database
    latest_saved_time = HepsiburadaDataReadOnly.query.with_entities(HepsiburadaDataReadOnly.saved_time) \
                                                     .order_by(HepsiburadaDataReadOnly.saved_time.desc()) \
                                                     .first()

    # If there is no data in the database, set the threshold time to the current time
    if not latest_saved_time:
        threshold_time = datetime.utcnow()
    else:
        # Calculate the time threshold for the last 40 minutes from the latest saved time
        threshold_time = latest_saved_time[0] - timedelta(minutes=40)

    # Fetch data from the read-only table (HepsiburadaDataReadOnly) using pagination and filtering by saved_time
    # Fetch data from the read-only table (HepsiburadaDataReadOnly) using pagination and filtering by saved_time
    all_notebooks = HepsiburadaDataReadOnly.query.filter(HepsiburadaDataReadOnly.saved_time >= threshold_time) \
                                                 .order_by(HepsiburadaDataReadOnly.saved_time.asc()) \
                                                 .offset(offset) \
                                                 .limit(items_per_page) \
                                                 .distinct() \
                                                 .all()

                                                 
    print(f"Number of elements returned: {len(all_notebooks)}")

    notebook_list = []
    for notebook in all_notebooks:
        # Create a dictionary with the required attributes for each notebook
        notebook_data = {
            "product_name": notebook.product_name,
            "brand_name": notebook.brand_name,
            "price": notebook.price,
            "review_rating": notebook.review_rating,
            "review_count": notebook.review_count,
            "product_link": notebook.product_link,
            "image_link": notebook.image_link,
            "fromWhere": notebook.fromWhere,
            "saved_time": notebook.saved_time.isoformat()  # Convert to ISO 8601 string format
        }
        notebook_list.append(notebook_data)

    # Return the list of notebooks as a JSON response
    return jsonify(notebook_list)