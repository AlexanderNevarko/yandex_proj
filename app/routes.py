from app import app
from app import api
from flask import jsonify, abort, request


@app.route('/')
@app.route('/index')
def index():
    return 'Привет Мир!'

@app.route('/imports', methods=['POST'])
def import_set():
    data = request.get_json() or {}
    if not data:
        abort(400)
    response, code = api.post(data)
    if code == 201:
        json_ = dict(data={'import_id': response})
        return jsonify(json_), 201
    else:
        abort(code)


@app.route('/imports/<int:import_id>/citizens/<int:citizen_id>', methods=['PATCH'])
def patch_citizen(import_id, citizen_id):
    changes = request.get_json() or {}
    if not changes:
        abort(400)
    response, code = api.patch(import_id=import_id, citizen_id=citizen_id, diff=changes)
    if code == 200:
        json_ = dict(data=response)
        return jsonify(json_), 200
    else:
        abort(code)


@app.route('/imports/<int:import_id>/citizens', methods=['GET'])
def get_set(import_id):
    response, code = api.get(import_id)
    if code == 200:
        json_ = dict(data=response)
        return jsonify(json_), 200
    else:
        abort(code)


@app.route('/imports/<int:import_id>/citizens/birthdays', methods=['GET'])
def get_presents(import_id):
    response, code = api.get_pres(import_id)
    if code == 200:
        json_ = dict(data=response)
        return jsonify(json_), 200
    else:
        abort(code)


@app.route('/imports/<int:import_id>/towns/stat/percentile/age', methods=['GET'])
def get_statistics(import_id):
    response, code = api.get_stat(import_id)
    if code == 200:
        json_ = dict(data=response)
        return jsonify(json_), 200
    else:
        abort(code)