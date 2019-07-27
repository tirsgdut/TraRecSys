from flask import Flask, jsonify, make_response, request, url_for
from flask_restful import Api, Resource
from wtforms import Form, StringField, DateField
from wtforms.validators import DataRequired
from subway import route_planning_subway
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app, resources=r'/*')
# deal with the cross-domain problem


@app.route('/todo/api/v1.0/route/try', methods=['GET'])
def get_task():
    return jsonify([{'start_x': 113.316113710606, 'start_y': 23.13371442727175,
                     'end_x': 113.3157526611475, 'end_y': 23.13371442727175},
                    {'start_x': 113.3157526611475, 'start_y': 23.122006234159915,
                     'end_x': 113.32688567240102, 'end_y': 23.122006234159915}]), 200


@app.route('/todo/api/v1.0/route', methods=['POST'])
def get_route():
    """
    get the post which should be the information of the departure and destination
    :return: a json form data which contain the route information
    """
    departure = request.form.get('departure', type=str, default=None)
    destination = request.form.get('destination', type=str, default=None)
    plan = route_planning_subway(departure, destination)
    return jsonify(plan)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)