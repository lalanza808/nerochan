from flask import Blueprint, jsonify


bp = Blueprint('api', 'api')

@bp.route('/api/test')
def get_prices():
    return jsonify({
        'test': True,
        'message': 'This is only a test.'
    })
