"""
application.py
==============
Runs the web app.
Endpoints and socket functions are declared below.
"""

from flask import (
    Flask, render_template, request, jsonify, flash,
    redirect, session, url_for
)
from flask_socketio import (
    SocketIO, join_room, leave_room, emit, rooms
)
import os
from werkzeug.utils import secure_filename


from src import data
from threading import Thread


app = Flask(__name__, template_folder="./templates", static_folder="./static")
app.secret_key = b"telemetry_secret_key"
app.config['UPLOAD_FOLDER'] = "/uploads"
socketio = SocketIO(app, logger=True)

rocket_data = data.DataHandler(False, is_sim=True)
update_data_thread = None
rocket_data_thread = None


@app.route("/")
def index():
    """
    Directs user to the main graphing page. http://127.0.0.1:5000/
    """
    return render_template(
        "pages/index.html",
        context={}
    )

@app.route("/settings", methods=["POST"])
def change_settings():
    """
    Post request handler for changing settings.
    """
    global rocket_data
    global update_data_thread
    if request.form["data_type"] in ["Demo Data", "Explore Data"]:
        if "file" in request.files:
            new_file = request.files["file"]
            filename = secure_filename(new_file.filename)
            new_file_name = os.path.join(
                os.getcwd(), app.config['UPLOAD_FOLDER'].strip("/"), filename
            )
            new_file.save(new_file_name)
            print("Uploaded:", new_file_name)

            if request.form["data_type"] == "Demo Data":
                rocket_data = data.DataHandler(False, filename=new_file_name, is_sim=True)
            if request.form["data_type"] == "Explore Data":
                rocket_data = data.DataHandler(False, filename=new_file_name, is_sim=False)

            data.should_kill_thread = True
            while data.should_kill_thread and update_data_thread != None:
                pass
            data.should_kill_thread = False
            print("Killed old thread")
            update_data_thread = Thread(target=data.update_data, args=(rocket_data,))
            #update_data_thread.daemon = True
            update_data_thread.start()
        else:
            print("NO FILE!")
    elif request.form["data_type"] == "Live Telemetry":
        print("Starting live data")
        rocket_data = data.DataHandler(True, is_sim=False)
        data.should_kill_thread = True
        while data.should_kill_thread and update_data_thread != None:
            pass
        data.should_kill_thread = False
        print("Killed old thread")
        update_data_thread = Thread(target=data.update_data, args=(rocket_data,))
        update_data_thread.daemon = True
        update_data_thread.start()
    else:
        pass
    return ('', 204)

@socketio.on("connected")
def connect_user():
    """
    Unused method for connected users.
    """
    return

@socketio.on("request_data")
def request_data():
    """
    Returns current data (if any) to the user that requested it.
    """
    global rocket_data
    d = rocket_data.get_data()
    emit("receive_data", d)

@socketio.on("halt")
def request_halt():
    """
    HALT state change to the rocket.
    """
    print("HALT!")
    rocket_data.halt()

@socketio.on("resume")
def request_resume():
    """
    RESUME state change to the rocket.
    """
    print("RESUME!")
    rocket_data.resume()

@socketio.on("demo_simulation")
def request_demo():
    """
    DEMO command to the rocket.
    """
    print("DEMO!")
    rocket_data.demo_simulation()

if __name__ == "__main__":
    socketio.run(app, debug=True)
