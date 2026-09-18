from database import get_db_connection


class PartiesRepository:

    @staticmethod
    def get_referentiel():
        conn = get_db_connection()
        cursor = conn.cursor()

        serveurs = [
            dict(r)
            for r in cursor.execute(
                "SELECT id, code, nom, region FROM serveurs"
            ).fetchall()
        ]
        jeux = [
            dict(r) for r in cursor.execute("SELECT id, nom FROM jeux").fetchall()
        ]
        files = [
            dict(r)
            for r in cursor.execute("SELECT id, jeu_id, nom FROM files").fetchall()
        ]
        annees_res = cursor.execute(
            "SELECT DISTINCT strftime('%Y', debut) AS annee FROM parties ORDER BY annee"
        ).fetchall()
        annees = [r["annee"] for r in annees_res if r["annee"] is not None]

        conn.close()
        return {
            "serveurs": serveurs,
            "jeux": jeux,
            "files": files,
            "annees": annees,
        }

    @staticmethod
    def get_parties(limit, offset, tri, ordre, filtres):
        champs_tri_map = {
            "date": "p.debut",
            "attente": "p.attente_secondes",
            "duree": "p.duree_minutes",
        }

        conn = get_db_connection()
        cursor = conn.cursor()

        conditions = []
        params = []

        if filtres.get("annee"):
            conditions.append("strftime('%Y', p.debut) = ?")
            params.append(str(filtres["annee"]))
        if filtres.get("serveur"):
            conditions.append("(s.code = ? OR s.nom = ? OR CAST(s.id AS TEXT) = ?)")
            params.extend([filtres["serveur"]] * 3)
        if filtres.get("jeu"):
            conditions.append("(j.nom = ? OR CAST(j.id AS TEXT) = ?)")
            params.extend([filtres["jeu"]] * 2)
        if filtres.get("file"):
            conditions.append("(f.nom = ? OR CAST(f.id AS TEXT) = ?)")
            params.extend([filtres["file"]] * 2)

        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

        # Nombre total d'éléments correspondant aux filtres
        count_query = f"""
            SELECT COUNT(*) as total
            FROM parties p
            JOIN serveurs s ON p.serveur_id = s.id
            JOIN files f ON p.file_id = f.id
            JOIN jeux j ON f.jeu_id = j.id
            {where_clause}
        """
        total = cursor.execute(count_query, params).fetchone()["total"]

        # Récupération de la page
        champ_tri = champs_tri_map[tri]
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
            ORDER BY {champ_tri} {ordre.upper()}
            LIMIT ? OFFSET ?
        """
        rows = cursor.execute(data_query, params + [limit, offset]).fetchall()
        conn.close()

        return [dict(row) for row in rows], total
