#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from flask import Flask, request
from .gen_report import process

def project_init():
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/<name>')
    def get_page(name):
        #Check that name is of of format YYYY_MM_DD_HH_MM_SS.html
        if not name.endswith(".html"):
            return "Invalid file name", 400
        name = name[:-5]
        if not name.replace("_", "").isdigit():
            return "Invalid file name", 400
        #Check that the name is a valid file
        if not os.path.exists(os.environ.get('REPORTS_DIR', "reports") + "/" + name + ".html"):
            return "File not found", 404
        #Read the file
        with open(os.environ.get('REPORTS_DIR', "reports") + "/" + name + ".html", "r") as file:
            return file.read(), 200
        
    
    @app.route('/', methods=['POST'])
    def process_page():
    # Get json from body
        try:
            my_json = json.dumps(request.get_json())
            
            filename = process(
                my_json,
                "/templates/"+os.environ.get('REPORT_TEMPLATE', "report_base.html"),
                os.environ.get('REPORTS_DIR', "/reports")
            )

            # Generate aux report
            process(
                my_json,
                "/templates/"+os.environ.get('GRAPHICS_REPORT_TEMPLATE', "report_commits_base.html"),
                os.environ.get('REPORTS_DIR', "/reports")
            )

            # print("http://localhost:5000/"+filename+".html", flush=True)
            #Return the link to the file
            return "http://localhost:5000/"+filename+".html", 200
        except Exception as e:
            return str(e), 500    
        
    return app