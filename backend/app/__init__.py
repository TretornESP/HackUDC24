#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, request
from .gen_report import process

def project_init():
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/<name>')
    def hello_world(name):
        #Check that name is only letters
        if not name.isalpha():
            return "Name must be letters only", 400
        #Check that the name is a valid file
        if not os.path.exists(os.environ.get('REPORTS_DIR', "reports") + "/" + name):
            return "File not found", 404
        #Return the file
        return app.send_static_file(os.environ.get('REPORTS_DIR', "reports") + "/" + name)
    
    @app.route('/', methods=['POST'])
    def test():
    # Get json from body
        try:
            filename = process(
                request.get_json(),
                "/templates/"+os.environ.get('REPORT_TEMPLATE', "report_base.html"),
                os.environ.get('REPORTS_DIR', "reports")
            )
            
            #Return the link to the file
            return "http://localhost:5000/"+filename, 200
        except Exception as e:
            return str(e), 500    
        

