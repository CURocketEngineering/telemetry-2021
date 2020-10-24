"""
application.py
==============
"""

from flask import (
    Flask, render_template, request, jsonify, flash,
    redirect, session, url_for
)
from flask_socketio import (
    SocketIO, join_room, leave_room, emit, rooms
)


app = Flask(__name__, template_folder="./templates", static_folder="./static")
app.secret_key = b"telemetry_secret_key"
socketio = SocketIO(app, logger=True)


@app.route("/")
def index():
    return render_template(
        "pages/index.html",
        context={}
    )

@socketio.on("connected")
def connect_user():
    #join_room("client")
    return

@socketio.on("request_data")
def request_data():
    emit("receive_data", {
        "data": [1, 2, 3]
    })


if __name__ == "__main__":
    socketio.run(app, debug=True)
