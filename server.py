from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

# Handle socket messages
@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected!")

# Listen for the 'update_message' event from the client
@socketio.on("update_message")
def handle_message(data):
    emit("update_message", data, broadcast=True)  # Emit back to all clients


if __name__ == "__main__":
    print("Flask server running on http://localhost:6464")
    socketio.run(app, host="0.0.0.0", port=6464)  # Explicitly set host and port here
