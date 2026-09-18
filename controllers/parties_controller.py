from flask import Blueprint, jsonify, request
from services.parties_service import PartiesService

parties_blueprint = Blueprint("parties", __name__, url_prefix="/api/v1/parties")


@parties_blueprint.route("/referentiel", methods=["GET"])
def get_referentiel():
    referentiel = PartiesService.get_referentiel()
    return jsonify(referentiel), 200


@parties_blueprint.route("", methods=["GET"])
def get_parties():
    try:
        resultat = PartiesService.get_parties(request.args)
        return jsonify(resultat), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
