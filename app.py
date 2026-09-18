import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DATABASE = "parties.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/api/v1/parties/referentiel", methods=["GET"])
def get_referentiel():
    conn = get_db_connection()
    cursor = conn.cursor()

    serveurs = [
        dict(r)
        for r in cursor.execute(
            "SELECT id, code, nom, region FROM serveurs"
        ).fetchall()
    ]
    jeux = [dict(r) for r in cursor.execute("SELECT id, nom FROM jeux").fetchall()]
    files = [
        dict(r)
        for r in cursor.execute("SELECT id, jeu_id, nom FROM files").fetchall()
    ]
    annees_res = cursor.execute(
        "SELECT DISTINCT strftime('%Y', debut) AS annee FROM parties ORDER BY annee"
    ).fetchall()
    annees = [r["annee"] for r in annees_res if r["annee"] is not None]

    conn.close()

    return jsonify(
        {"serveurs": serveurs, "jeux": jeux, "files": files, "annees": annees}
    )


@app.route("/api/v1/parties", methods=["GET"])
def get_parties():
    # Validation des arguments de pagination
    try:
        limit = int(request.args.get("limit", 20))
        offset = int(request.args.get("offset", 0))
        if limit < 1 or offset < 0:
            raise ValueError()
    except ValueError:
        return (
            jsonify(
                {"error": "Les paramètres 'limit' et 'offset' doivent être des entiers positifs."}
            ),
            400,
        )

    # Validation du tri
    tri = request.args.get("tri", "date")
    ordre = request.args.get("ordre", "asc").lower()

    champs_tri_valides = {
        "date": "p.debut",
        "attente": "p.attente_secondes",
        "duree": "p.duree_minutes",
    }
    if tri not in champs_tri_valides:
        return (
            jsonify(
                {
                    "error": f"Colonne de tri inconnue: '{tri}'. Valeurs acceptées : {list(champs_tri_valides.keys())}"
                }
            ),
            400,
        )

    if ordre not in ["asc", "desc"]:
        return (
            jsonify(
                {
                    "error": f"Ordre de tri invalide: '{ordre}'. Valeurs acceptées : ['asc', 'desc']"
                }
            ),
            400,
        )

    # Récupération des filtres
    annee = request.args.get("annee")
    serveur = request.args.get("serveur")
    jeu = request.args.get("jeu")
    file_id = request.args.get("file")

    conn = get_db_connection()
    cursor = conn.cursor()

    conditions = []
    params = []

    if annee:
        conditions.append("strftime('%Y', p.debut) = ?")
        params.append(str(annee))
    if serveur:
        conditions.append("(s.code = ? OR s.nom = ? OR CAST(s.id AS TEXT) = ?)")
        params.extend([serveur, serveur, serveur])
    if jeu:
        conditions.append("(j.nom = ? OR CAST(j.id AS TEXT) = ?)")
        params.extend([jeu, jeu])
    if file_id:
        conditions.append("(f.nom = ? OR CAST(f.id AS TEXT) = ?)")
        params.extend([file_id, file_id])

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

    # Requête de comptage du total
    count_query = f"""
        SELECT COUNT(*) as total
        FROM parties p
        JOIN serveurs s ON p.serveur_id = s.id
        JOIN files f ON p.file_id = f.id
        JOIN jeux j ON f.jeu_id = j.id
        {where_clause}
    """
    total = cursor.execute(count_query, params).fetchone()["total"]

    # Requête de récupération des données paginées
    data_query = f"""
        SELECT 
            p.id, 
            s.code AS serveur, 
            j.nom AS jeu, 
            f.nom AS file, 
            p.debut, 
            p.attente_secondes, 
            p.duree_minutes
        FROM parties p
        JOIN serveurs s ON p.serveur_id = s.id
        JOIN files f ON p.file_id = f.id
        JOIN jeux j ON f.jeu_id = j.id
        {where_clause}
        ORDER BY {champs_tri_valides[tri]} {ordre.upper()}
        LIMIT ? OFFSET ?
    """
    query_params = params + [limit, offset]
    rows = cursor.execute(data_query, query_params).fetchall()
    conn.close()

    data = [dict(row) for row in rows]

    return jsonify(
        {"data": data, "total": total, "limit": limit, "offset": offset}
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)