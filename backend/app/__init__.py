#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
MIT License

Copyright (c) 2024 codeegenerates

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os
import json
from flask import Flask, request
from .gen_report import process
from .report_commits_gen import process_second

def project_init():
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/<name>')
    def get_page(name):
        #Check that name is of of format YYYY_MM_DD_HH_MM_SS.html
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
            process_second(
                my_json,
                "/templates/"+os.environ.get('GRAPHICS_REPORT_TEMPLATE', "report_commits_base.html"),
                os.environ.get('REPORTS_DIR', "/reports")
            )

            # print("http://localhost:5000/"+filename+".html", flush=True)
            #Return the link to the file
            return "https://localhost:4043/"+filename, 200
        except Exception as e:
            return str(e), 500    
        
    return app