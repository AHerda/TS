from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    headers = dict(request.headers)
    return str(headers)
    #return "Hello World!"

if __name__ == "__main__":
    app.run()