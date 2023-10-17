"""
Elizabeth Bowden's Flask API.
"""

from flask import Flask, abort, send_from_directory, render_template

import os
import configparser

# get configuration info
def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

config = parse_config(["credentials.ini", "default.ini"])
port_config = config["SERVER"]["PORT"]
debug_config = config["SERVER"]["DEBUG"]
DOCKROOT = config["SERVER"]["DOCKROOT"]


app = Flask(__name__)

HOME = """
    <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
    <html> <head>
    </head>

    <body>
    <p>
    Home page
    </p>

    </body>
    </html>
"""

@app.route("/")
def index():
    # empty requests get served with a homepage
    return HOME

@app.route("/<string:filename>")
def get_file(filename):
    # check if it is a valid file
    if os.path.isfile(os.getcwd() + '/pages/' + filename):
        #if the file exist it will be served
        return send_from_directory(os.getcwd() + '/pages/', path=filename, as_attachment=False), 200
    else:
        #if there is an illegal character (~ and ..) it will respond with error 403 page
        if ("~" in filename or ".." in filename):
           return send_from_directory('pages/', '403.html'), 403 
        else:
        #if a user requests a file that doesn't exist with no
        #illegal characters they'll get a 404 error page
            return send_from_directory('pages/', '404.html'), 404

if __name__ == "__main__":
    app.run(debug=debug_config, host='0.0.0.0', port=port_config)