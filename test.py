from flask import Flask, render_template, request,jsonify

app = Flask(__name__)
@app.route("/")
def SayHello():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)
