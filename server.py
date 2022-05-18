from flask import Flask, render_template
from model import connect_to_db, db


app = Flask(__name__)


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)