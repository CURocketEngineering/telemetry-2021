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

from src import data
from threading import Thread


app = Flask(__name__, template_folder="./templates", static_folder="./static")
app.secret_key = b"telemetry_secret_key"
socketio = SocketIO(app, logger=True)

rocket_data = data.DataHandler(False, is_sim=True)  # DEBUG
update_data_thread = Thread(target=data.update_data, args=(rocket_data,))
update_data_thread.daemon = True
update_data_thread.start()


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
    d = rocket_data.get_data()
    print(d)
    emit("receive_data", d)


if __name__ == "__main__":
    socketio.run(app, debug=True)
