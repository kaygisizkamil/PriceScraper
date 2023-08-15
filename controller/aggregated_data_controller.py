from flask import Blueprint, jsonify
from model.data_from_different_sources import From_different_sourcesReadOnly
from flask import Blueprint, jsonify, request,json
from datetime import datetime, timedelta
from flask import jsonify, make_response
from sqlalchemy import func
from model.dbmodel import db
from sqlalchemy import func,or_,and_, cast,text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import  distinct
from sqlalchemy import select, desc, text, func,asc,column
from sqlalchemy import text
from fuzzywuzzy import fuzz



all_brands_blueprint = Blueprint('unique_brands', __name__)
all_processors_blueprint = Blueprint('all_processors', __name__)
all_rams_blueprint=Blueprint('all_rams', __name__)
all_screen_sizes_blueprint=Blueprint('all_screens',__name__)
all_cheapest_computers_blueprint=Blueprint('all_cheapests',__name__)
all_price_range_blueprint = Blueprint('all_price_range', __name__)
all_sidebar_computers_blueprint=Blueprint('/sidebar/getall',__name__)
all_matched_computers_blueprint = Blueprint('all_matched_computers_blueprint', __name__)




@all_brands_blueprint.route('/checkbox-options/getall', methods=['GET'])
def get_distinct_checkbox_options():
    try:
        # Calculate the threshold time for the last 40 minutes
        threshold_time = datetime.utcnow() - timedelta(minutes=5000)

        # Retrieve distinct checkbox options saved in the last 40 minutes
        distinct_brands = db.db.session.query(From_different_sourcesReadOnly.brand_name.distinct()) \
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
            processor_options = db.db.session.query(func.trim(From_different_sourcesReadOnly.cpu).label('processor')) \
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
            ram_options = db.db.session.query(func.trim(From_different_sourcesReadOnly.ram).label('ram')) \
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
            screen_size_options = db.db.session.query(func.trim(From_different_sourcesReadOnly.screen).label('screen')) \
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
#it was real challenging to do it using orm so i used raw sql
@all_cheapest_computers_blueprint.route('/cheapest/getall', methods=['GET'])
def get_cheapest_options():
    # Define the number of items per page
    items_per_page = 20

    # Calculate the page number and offset
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * items_per_page

    # Get the user's selected sorting option and handle default case
    selected_sort_option = request.args.get('sort', 'ascendive_price')

    # Determine which query to use based on the sorting option
    if selected_sort_option == 'ascendive_price':
        order_by_column = "price ASC"
    elif selected_sort_option == 'descending_price':
        order_by_column = "price DESC"
    elif selected_sort_option == 'descendive_review_rating':
        order_by_column = "review_rating ASC"
    elif selected_sort_option == 'ascendive_review_count':
        order_by_column = "review_count DESC"
    elif selected_sort_option == 'descendive_review_count':
        order_by_column = "review_count ASC"
    elif selected_sort_option == 'ascendive_review_rating':
        order_by_column = "review_rating DESC"
    else:
        return jsonify({"error": "Invalid sorting option"})

    # Construct the final query with pagination and sorting
    pagination_query = f"""
        WITH ranked AS (
            SELECT
                *,
                ROW_NUMBER() OVER (PARTITION BY product_name ORDER BY {order_by_column}) AS rn
            FROM from_different_sources
        )
        SELECT *
        FROM ranked fds 
        WHERE rn = 1
        ORDER BY {order_by_column}
        LIMIT :limit OFFSET :offset;
    """

    # Execute the selected query using SQLAlchemy's text function
    query_results = db.session.execute(text(pagination_query), {'limit': items_per_page, 'offset': offset}).fetchall()


    # Prepare the results for JSON response
    notebook_list = []
    for notebook in query_results:
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


@all_price_range_blueprint.route('/price-range/get', methods=['GET'])
def get_price_range():
    try:
        selected_brand = request.args.get('brand')  # Get the selected brand from query parameter
        threshold_time = datetime.utcnow() - timedelta(minutes=5000)

        # Retrieve the minimum and maximum prices for the selected brand saved in the last 40 minutes
        price_range = db.db.session.query(
            func.min(From_different_sourcesReadOnly.price).label('min_price'),
            func.max(From_different_sourcesReadOnly.price).label('max_price')
        ).filter(From_different_sourcesReadOnly.saved_time >= threshold_time) \
         .filter(func.lower(From_different_sourcesReadOnly.brand_name) == selected_brand.lower()) \
         .first()

        response_data = {
            'minPrice': price_range.min_price if price_range.min_price else 0,
            'maxPrice': price_range.max_price if price_range.max_price else 200000
        }
        response = make_response(jsonify(response_data), 200)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        response_data = {'error': error_message}
        response = make_response(jsonify(response_data), 500)

    return response


'''
SELECT *
FROM From_different_sourcesReadOnly AS main
JOIN (
    SELECT
        product_name,
        brand_name,
        MAX(saved_time) AS latest_saved_time
    FROM From_different_sourcesReadOnly
    WHERE saved_time >= (NOW() - INTERVAL 5000 MINUTE) 
    GROUP BY product_name, brand_name
) AS subquery
ON main.product_name = subquery.product_name
   AND main.brand_name = subquery.brand_name
   AND main.saved_time = subquery.latest_saved_time
WHERE main.saved_time >= (NOW() - INTERVAL 5000 MINUTE) ORDER BY main.price ASC, main.saved_time ASC
LIMIT items_per_page OFFSET offset;
'''
@all_sidebar_computers_blueprint.route('/sidebar/getall', methods=['GET'])
def get_sidebar_options():
    # Get selected values from query parameters
    selected_values = request.args.get('selectedValues', '{}')
    selected_values = json.loads(selected_values)
    selected_column_mappings = {
        'brands': 'brand_name',
        'processors': 'cpu',
        'rams': 'ram',
        'screenSizes': 'screen',
        'priceInterval': 'price'
        # Add other mappings as needed
    }

    base_query = """
        SELECT *
        FROM from_different_sources fds
        WHERE (fds.product_name, fds.brand_name, fds.saved_time) IN (
            SELECT
                product_name,
                brand_name,
                MAX(saved_time) AS latest_saved_time
            FROM from_different_sources
            GROUP BY product_name, brand_name
        )
    """
    params = {}

    brands = selected_values.get('brands')
    processors = selected_values.get('processors')
    rams = selected_values.get('rams')
    screen_sizes = selected_values.get('screenSizes')
    price_interval = selected_values.get('priceInterval')

    if brands:
        base_query += f" AND {selected_column_mappings['brands']} = ANY(:brands)"
        params['brands'] = brands
    if processors:
        processor_conditions = []
        for processor in processors:
            processor_condition = f"cpu ILIKE '%{processor}%'"
            processor_conditions.append(processor_condition)
        processor_condition = " OR ".join(processor_conditions)
        base_query += f" AND ({processor_condition})"
    if rams:
        advanced_ram_conditions = []
        for ram in rams:
            # Remove the "+" sign and convert to lowercase before querying
            ram = ram.replace('+', '').lower()
            ram_condition = f"ram ILIKE '%{ram}%'"
            advanced_ram_conditions.append(ram_condition)
        ram_condition = " OR ".join(advanced_ram_conditions)
        base_query += f" AND ({ram_condition})"
    if screen_sizes:
        advanced_screen_conditions = []
        for screen_size in screen_sizes:
            # Remove the "+" sign and convert to lowercase before querying
            screen_size = screen_size.replace('+', '').lower()
            screen_condition = f"screen ILIKE '%{screen_size}%'"
            advanced_screen_conditions.append(screen_condition)
        screen_condition = " OR ".join(advanced_screen_conditions)
        base_query += f" AND ({screen_condition})"
    if price_interval:
        base_query += " AND price BETWEEN :min_price AND :max_price"
        params['min_price'] = price_interval[0]
        params['max_price'] = price_interval[1]

    # Get the user's selected sorting option and handle default case
    selected_sort_option = request.args.get('sort', 'ascendive_price')

    # Determine which query to use based on the sorting option
    if selected_sort_option == 'ascendive_price':
        order_by_column = "price ASC"
    elif selected_sort_option == 'descending_price':
        order_by_column = "price DESC"
    elif selected_sort_option == 'descendive_review_rating':
        order_by_column = "review_rating ASC"
    elif selected_sort_option == 'ascendive_review_count':
        order_by_column = "review_count DESC"
    elif selected_sort_option == 'descendive_review_count':
        order_by_column = "review_count ASC"
    elif selected_sort_option == 'ascendive_review_rating':
        order_by_column = "review_rating DESC"
    else:
        return jsonify({"error": "Invalid sorting option"})

    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('itemsPerPage', 20, type=int)  # Get items per page from query parameters
    base_query += f" ORDER BY {order_by_column} LIMIT :limit OFFSET :offset"
    params['limit'] = items_per_page
    params['offset'] = (page - 1) * items_per_page

    query_results = db.session.execute(text(base_query), params).fetchall()

    # Prepare the results for JSON response
    notebook_list = []
    for notebook in query_results:
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


@all_matched_computers_blueprint.route('/matched/getall', methods=['GET'])
def get_matched_options():
    # Define the number of items per page and the larger batch size
    items_per_page = 20
    larger_batch_size = 100  # Adjust this based on your needs

    # Calculate the page number and offset
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * items_per_page

    # Get the user's selected sorting option and handle default case
    selected_sort_option = request.args.get('sort', 'ascendive_price')

    # Determine which query to use based on the sorting option
    if selected_sort_option == 'ascendive_price':
        order_by_column = "price ASC"
    elif selected_sort_option == 'descending_price':
        order_by_column = "price DESC"
    elif selected_sort_option == 'descendive_review_rating':
        order_by_column = "review_rating ASC"
    elif selected_sort_option == 'ascendive_review_count':
        order_by_column = "review_count DESC"
    elif selected_sort_option == 'descendive_review_count':
        order_by_column = "review_count ASC"
    elif selected_sort_option == 'ascendive_review_rating':
        order_by_column = "review_rating DESC"
    else:
        return jsonify({"error": "Invalid sorting option"})

    # Get the user's search query
    user_query = request.args.get('query', '')

    # Construct the base query with larger batch size, pagination, and sorting
    base_query = f"""
        WITH ranked AS (
            SELECT
                *,
                ROW_NUMBER() OVER (PARTITION BY product_name ORDER BY {order_by_column}) AS rn
            FROM from_different_sources
            WHERE LOWER(product_name) LIKE LOWER(:query)
        )
        SELECT *
        FROM ranked
        WHERE rn = 1
        ORDER BY {order_by_column}
        LIMIT {larger_batch_size};
    """

    # Execute the base query using SQLAlchemy's text function
    query_results = db.session.execute(text(base_query), {'query': f'%{user_query}%'}).fetchall()

    # Prepare the results for fuzzy search
    data_for_fuzzy_search = []
    for notebook in query_results:
        data_for_fuzzy_search.append({
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
        })

    # Perform fuzzy search and filtering
    matching_results = []
    for item in data_for_fuzzy_search:
        match_ratio = fuzz.partial_ratio(user_query.lower(), item['product_name'].lower())  # Compare input with the product name
        if match_ratio > 70:  # Adjust the threshold as needed
            matching_results.append(item)

    # Return the paginated fuzzy search results as a JSON response
    paginated_results = matching_results[offset:offset + items_per_page]
    return jsonify(paginated_results)