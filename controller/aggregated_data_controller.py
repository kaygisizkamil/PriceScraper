from flask import Blueprint, jsonify
from model.data_from_different_sources import From_different_sourcesReadOnly
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask import jsonify, make_response
from sqlalchemy import func
from model.dbmodel import db
from sqlalchemy import func,or_,and_, cast,text
from sqlalchemy.dialects.postgresql import ARRAY

all_brands_blueprint = Blueprint('unique_brands', __name__)
all_processors_blueprint = Blueprint('all_processors', __name__)
all_rams_blueprint=Blueprint('all_rams', __name__)
all_screen_sizes_blueprint=Blueprint('all_screens',__name__)
all_cheapest_computers_blueprint=Blueprint('all_cheapests',__name__)



@all_brands_blueprint.route('/checkbox-options/getall', methods=['GET'])
def get_distinct_checkbox_options():
    try:
        # Calculate the threshold time for the last 40 minutes
        threshold_time = datetime.utcnow() - timedelta(minutes=5000)

        # Retrieve distinct checkbox options saved in the last 40 minutes
        distinct_brands = db.session.query(From_different_sourcesReadOnly.brand_name.distinct()) \
            .filter(From_different_sourcesReadOnly.saved_time >= threshold_time) \
            .all()

        distinct_brands = [brand[0] for brand in distinct_brands]

        # Create a response object with JSON data
        response_data = {'brands': distinct_brands}
        response = make_response(jsonify(response_data), 200)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        response_data = {'error': error_message}
        response = make_response(jsonify(response_data), 500)

    return response #{"brands":["Asus","Macbook","Msi","Casper","Huawei","Lenovo","MacBook","Hp","Dell","Acer"]}


@all_processors_blueprint.route('/processor-options/getall', methods=['GET'])
def get_processor_options():
    try:
        selected_brands = request.args.getlist('brand')  # Get the list of selected brands from query parameters

        if selected_brands:
            threshold_time = datetime.utcnow() - timedelta(minutes=5000)
            keyword_list = ['intel', 'amd', 'm1', 'm2']

            # Retrieve distinct processor options for the selected brands saved in the last 40 minutes
            processor_options = db.session.query(func.trim(From_different_sourcesReadOnly.cpu).label('processor')) \
                                .filter(From_different_sourcesReadOnly.saved_time >= threshold_time) \
                                .filter(func.lower(From_different_sourcesReadOnly.brand_name).in_([brand.lower() for brand in selected_brands])) \
                                .filter(or_(*[text("lower(from_different_sources.cpu) SIMILAR TO '%(" + keyword + ")%'") for keyword in keyword_list])) \
                                .distinct() \
                                .all()
            
            valid_processors = set()
            
            # Process the processor options to include only 'intel', 'amd', 'm1', 'm2'
            for option in processor_options:
                for keyword in keyword_list:
                    if keyword in option[0].lower():
                        valid_processors.add(keyword)
                        break
            
            response_data = {'processorOptions': list(valid_processors)}
            response = make_response(jsonify(response_data), 200)
        else:
            response_data = {'error': 'Selected brands not provided'}
            response = make_response(jsonify(response_data), 400)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        response_data = {'error': error_message}
        response = make_response(jsonify(response_data), 500)

    return response
@all_rams_blueprint.route('/ram-options/getall', methods=['GET'])
def get_ram_options():
    try:
        selected_brands = request.args.getlist('brand')  # Get the list of selected brands from query parameters

        if selected_brands:
            threshold_time = datetime.utcnow() - timedelta(minutes=5000)

            # Retrieve distinct RAM options for the selected brands saved in the last 40 minutes
            ram_options = db.session.query(func.trim(From_different_sourcesReadOnly.ram).label('ram')) \
                .filter(From_different_sourcesReadOnly.saved_time >= threshold_time) \
                .filter(func.lower(From_different_sourcesReadOnly.brand_name).in_([brand.lower() for brand in selected_brands])) \
                .distinct() \
                .all()

            valid_rams = [ram[0] for ram in ram_options]

            response_data = {'ramOptions': valid_rams}
            response = make_response(jsonify(response_data), 200)
        else:
            response_data = {'error': 'Selected brands not provided'}
            response = make_response(jsonify(response_data), 400)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        response_data = {'error': error_message}
        response = make_response(jsonify(response_data), 500)
    print(response)
    return response
@all_screen_sizes_blueprint.route('/screen-size-options/getall', methods=['GET'])
def get_screen_size_options():
    try:
        selected_brands = request.args.getlist('brand')  # Get the list of selected brands from query parameters

        if selected_brands:
            threshold_time = datetime.utcnow() - timedelta(minutes=5000)

            # Retrieve distinct screen sizes for the selected brands saved in the last 40 minutes
            screen_size_options = db.session.query(func.trim(From_different_sourcesReadOnly.screen).label('screen')) \
                .filter(From_different_sourcesReadOnly.saved_time >= threshold_time) \
                .filter(func.lower(From_different_sourcesReadOnly.brand_name).in_([brand.lower() for brand in selected_brands])) \
                .distinct() \
                .all()

            valid_screen_sizes = [size[0] for size in screen_size_options]

            response_data = {'screenSizeOptions': valid_screen_sizes}
            response = make_response(jsonify(response_data), 200)
        else:
            response_data = {'error': 'Selected brands not provided'}
            response = make_response(jsonify(response_data), 400)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        response_data = {'error': error_message}
        response = make_response(jsonify(response_data), 500)
    
    print(response)
    return response
@all_cheapest_computers_blueprint.route('/cheapest/getall', methods=['GET'])
@all_cheapest_computers_blueprint.route('/cheapest/getall', methods=['GET'])
def get_cheapest_options():
    page = request.args.get('page', 1, type=int)
    
    # Number of items per page (adjust this value based on your requirements)
    items_per_page = 20

    # Calculate the offset to fetch the data for the requested page
    offset = (page - 1) * items_per_page
    latest_saved_time = From_different_sourcesReadOnly.query.with_entities(From_different_sourcesReadOnly.saved_time) \
                                                     .order_by(From_different_sourcesReadOnly.saved_time.desc()) \
                                                     .first()
    
    if not latest_saved_time:
        threshold_time = datetime.utcnow()
    else:
        # Calculate the time threshold for the last 40 minutes from the latest saved time
        threshold_time = latest_saved_time[0] - timedelta(minutes=5000)

    # Fetch the cheapest notebooks within the threshold time
    cheapest_notebooks_subquery = From_different_sourcesReadOnly.query \
        .filter(From_different_sourcesReadOnly.saved_time >= threshold_time) \
        .order_by(
            From_different_sourcesReadOnly.product_name,
            From_different_sourcesReadOnly.brand_name,
            From_different_sourcesReadOnly.saved_time.desc()
        ) \
        .group_by(
            From_different_sourcesReadOnly.product_name,
            From_different_sourcesReadOnly.brand_name
        ).subquery()

    latest_saved_times = db.session.query(
        From_different_sourcesReadOnly.product_name,
        From_different_sourcesReadOnly.brand_name,
        func.max(From_different_sourcesReadOnly.saved_time).label('latest_saved_time')
    ).group_by(
        From_different_sourcesReadOnly.product_name,
        From_different_sourcesReadOnly.brand_name
    ).subquery()

    result = db.session.query(
        From_different_sourcesReadOnly
    ).join(
        latest_saved_times,
        and_(
            From_different_sourcesReadOnly.product_name == latest_saved_times.c.product_name,
            From_different_sourcesReadOnly.brand_name == latest_saved_times.c.brand_name,
            From_different_sourcesReadOnly.saved_time == latest_saved_times.c.latest_saved_time
        )
    ).filter(
        From_different_sourcesReadOnly.saved_time >= threshold_time
    ).order_by(
        From_different_sourcesReadOnly.price.asc(),
        From_different_sourcesReadOnly.saved_time.asc()
    ).limit(items_per_page).offset(offset).all()

    notebook_list = []
    for notebook in result:
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
            "cpu": notebook.cpu,
            "ram": notebook.ram,
            "screen": notebook.screen,
            "gpu": notebook.gpu,
            "os": notebook.os,
            "ssd": notebook.ssd,
            "hdd": notebook.hdd,
            "saved_time": notebook.saved_time.isoformat()  # Convert to ISO 8601 string format
        }
        notebook_list.append(notebook_data)

    # Return the list of notebooks as a JSON response
    return jsonify(notebook_list)
