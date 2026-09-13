from flask import Flask, render_template, jsonify
from data_store import get_packets
from sniffer import run_sniffer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    return jsonify(get_packets())

if __name__ == "__main__":

    run_sniffer()   # start live capture
    app.run(debug=True, use_reloader=False)