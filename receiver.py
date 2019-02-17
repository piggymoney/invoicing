

from flask import Flask, request


def create_app():
    app = Flask('receiver')

    @app.route('/', methods=['POST'])
    def receive_call():
        print("Got request: {0}".format(request.json))

        return "", 200

    return app
