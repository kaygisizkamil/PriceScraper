from flask import Blueprint, jsonify
from model.hepsiburda_datas import HepsiburadaDataReadOnly

hepsiburada_blueprint = Blueprint('hepsiburada', __name__)

# Define the route
@hepsiburada_blueprint.route('/api/hepsiburada/notebooks/getall', methods=['GET'])
def get_all_notebooks():
    # Fetch data from the read-only table (HepsiburadaDataReadOnly)
    all_notebooks = HepsiburadaDataReadOnly.query.all()

    notebook_list = []
    for notebook in all_notebooks:
        notebook_data = {
            "product_name": notebook.product_name,
            "brand_name": notebook.brand_name,
            "price": notebook.price,
            "review_rating": notebook.review_rating,
            "review_count": notebook.review_count,
            "product_link": notebook.product_link,
            "image_link": notebook.image_link,
            "fromWhere": notebook.fromWhere,
            "saved_time": notebook.saved_time
        }
        notebook_list.append(notebook_data)

    return jsonify(notebook_list)