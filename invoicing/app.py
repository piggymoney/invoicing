
from __future__ import absolute_import

from flask import Flask, jsonify
from flask.json import JSONDecoder

from . import db, invoices


class CustomJSONDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        kwargs['parse_float'] = str

        super(CustomJSONDecoder, self).__init__(*args, **kwargs)


def create_app():
    app = Flask('invoicing')
    app.json_decoder = CustomJSONDecoder

    init_db(app)

    @app.route('/')
    def index():
        return jsonify({'hello': 'hi'})

    app.register_blueprint(invoices.blueprint, url_prefix='/invoices')

    return app


def init_db(app):
    db.init(app.config.get('DATABASE_PATH', 'db.sqlite'))
