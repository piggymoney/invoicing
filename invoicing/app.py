
from __future__ import absolute_import

from flask import Flask, jsonify
from flask.json import JSONDecoder


class CustomJSONDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        kwargs['parse_float'] = str

        super(CustomJSONDecoder, self).__init__(*args, **kwargs)


def create_app():
    app = Flask('invoicing')
    app.json_decoder = CustomJSONDecoder

    @app.route('/')
    def index():
        return jsonify({'hello': 'hi'})

    return app
