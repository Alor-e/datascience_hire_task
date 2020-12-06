import os
import re
from flask import Flask, jsonify, request
from api_generator import links_recommender
from sql_database import store_user_data

app = Flask(__name__)


@app.route('/api/recommend', methods=['GET'])
def recommender_response():
    """
    Returns JSON response of recommender
    """
    link_url = request.args.get('link')
    phone_number = request.args.get('phone')

    if link_url and re.search('jumia.com.ng', link_url):
        output = links_recommender(link_url)
    else:
        output = {'error': 'url not valid'}
    response = jsonify(output)

    if phone_number:
        store_user_data(phone_number, link_url)

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
