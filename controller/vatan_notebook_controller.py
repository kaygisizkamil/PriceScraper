# controllers/vatan_notebook_controller.py
from flask import Blueprint, jsonify
from model.vatandatas import VatanDataReadOnly

vatan_blueprint = Blueprint('vatan', __name__)

# Define the route
@vatan_blueprint.route('/api/vatan/notebooks/getall', methods=['GET'])
def vatan_get_all_notebooks():
    # Fetch data from the read-only table (ProductDataReadOnly)
    all_notebooks = VatanDataReadOnly.query.all()

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