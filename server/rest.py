from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
info_list = {}

@app.route("/<server_id>/")
def get_data(server_id: str):
    if server_id in info_list:
        return info_list[server_id]
    return {}

@app.route("/<server_id>/", methods=['POST'])
def set_data(server_id: str):
    global info_list
    body = request.get_json()
    if body is not None:
        info_list[server_id] = body
    return body or {}

@app.route("/")
def get_all_data():
    return info_list