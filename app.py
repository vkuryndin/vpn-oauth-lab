from flask import Flask, render_template
import platform
import socket

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/page1")
def page1():
    return render_template("page1.html")


@app.route("/page2")
def page2():
    return render_template("page2.html")

@app.route("/info")
def info():
    return render_template(
        "info.html",
        hostname=socket.gethostname(),
        os_name=platform.system(),
        os_version=platform.release(),
        python_version=platform.python_version()
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)