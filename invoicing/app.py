
from __future__ import absolute_import

from flask import Flask, jsonify


def create_app():
    app = Flask('invoicing')

    @app.route('/')
    def index():
        return jsonify({'hello': 'hi'})

    return app
