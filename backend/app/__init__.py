import json
from flask import Flask, request


def project_init():
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    
    @app.route('/test', methods=['POST'])
    def test():
    # Get json from body
        data = request.get_json()
        print(data, flush=True)
        return str(data)
    
    return app