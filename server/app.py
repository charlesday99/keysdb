from flask import redirect, url_for, render_template, abort, send_from_directory, request, jsonify, send_file
from flask import Flask

from gevent.pywsgi import WSGIServer
import keys_server
import json
import time
import os

# Create app
app = Flask(__name__,static_url_path='')
app.debug = False

# Create key-value database
KeysDB = keys_server.KeysDB(
    os.path.join("static","keyvalues.db")
)


# Landing page
@app.route('/')
def start_page():
    return render_template(
        'keys.html',
        connections=len(KeysDB.getConnections())
    )


# Key-Value Database route and logic
@app.route('/key/<string:key>', methods=["POST", "GET", "PUT", "DELETE"])
def keys(key):
    if request.method == 'GET':
        if KeysDB.hasKey(key):
            result = KeysDB.getValue(key)
            if result[1][:5] == "@url:":
                return redirect(result[1][5:],code=302)
            else:
                return jsonify(key=result[0], value=result[1], modified=result[2], action="GET", status="OK")
        else:
            return jsonify(status="ERROR", key=key, action="GET", message="Key not found."), 404

    if request.method == 'DELETE':
        if KeysDB.hasKey(key):
            result = KeysDB.deleteKey(key)
            return jsonify(key=result, action="DELETE", status="OK")
        else:
            return jsonify(status="ERROR", key=key, action="DELETE", message="Key not found."), 404

    if request.method == 'POST' or request.method == 'PUT':
        value=request.json['value']
        if value != None:
            if len(value) <= keys_server.MAX_LENGTH:
                result = KeysDB.setValue(key, value)
                return jsonify(key=result[0], value=result[1], modified=result[2], status="OK", action=request.method)
            else:
                return jsonify(status="ERROR", message="Value entered is too long. Please enter a value less then 1000 characters.", key=key, action=request.method), 400
        else:
            return jsonify(status="ERROR", message="No value submitted. Please enter both a Key and a Value.", key=key, action=request.method), 400
        
    return jsonify(status="ERROR", message="Unsupported HTTP Method. Please use either PUT, POST, GET or DELETE.", key=key, action="UNKNOWN"), 400


# Handle 400 Error
@app.errorhandler(400)
def error_400(e):
    return render_template('error.html',
                           code=400,
                           about="Invalid request, try again with different values!"),400


# Handle 404 Error
@app.errorhandler(404)
def error_404(e):
    return render_template('error.html',
                           code=404,
                           about="The file/service was not found, try again!"),404


# Handle 418 Error
@app.errorhandler(418)
def error_418(e):
    return render_template('error.html',
                           code=418,
                           about="I'm a teapot. This server is a teapot, not a coffee machine."),418


# Handle 500 Error
@app.errorhandler(500)
def error_500(e):
    return render_template('error.html',
                           code=500,
                           about="Something on the server went very wrong, Sorry!"),500


# Serve favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Start point
if __name__ == "__main__":
    print("Operating system: {}".format(os.name))
    
    if os.name == "posix":
        #Linux, run on port 8080
        http_server = WSGIServer(('0.0.0.0', 8080), app)
        print("Loaded as HTTP Server on port 8080, running forever:")
        http_server.serve_forever()
    else:
        #Windows, run on port 80
        http_server = WSGIServer(('0.0.0.0', 80), app)
        print("Loaded as HTTP Server on port 80, running forever:")
        http_server.serve_forever()
