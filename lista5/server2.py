from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/<path:path>")
def serve_file(path):
    print(path)
    return send_from_directory("./strona", path)

@app.route("/")
def index():
    return send_from_directory("./strona", "index.html")

if __name__ == "__main__":
    app.run()