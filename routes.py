from flask import Flask, render_template, request

app = Flask(__name__)

app.secret_key = "development-key"

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
