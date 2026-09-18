from flask import Flask, jsonify
from controllers.parties_controller import parties_blueprint

app = Flask(__name__)

# Enregistrement du Blueprint
app.register_blueprint(parties_blueprint)


@app.route("/")
def index():
    return jsonify({"message": "API R5C4 - Pilotage des files de jeu", "version": "v1"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
