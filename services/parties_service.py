from repositories.parties_repository import PartiesRepository


class PartiesService:

    @staticmethod
    def get_referentiel():
        return PartiesRepository.get_referentiel()

    @staticmethod
    def get_parties(params):
        # 1. Validation de la pagination
        try:
            limit = int(params.get("limit", 20))
            offset = int(params.get("offset", 0))
            if limit < 1 or offset < 0:
                raise ValueError()
        except ValueError:
            raise ValueError("Les paramètres 'limit' et 'offset' doivent être des entiers positifs.")

        # 2. Validation du tri
        tri = params.get("tri", "date")
        ordre = params.get("ordre", "asc").lower()
        valeurs_tri_valides = ["date", "attente", "duree"]

        if tri not in valeurs_tri_valides:
            raise ValueError(f"Colonne de tri inconnue: '{tri}'. Valeurs acceptées : {valeurs_tri_valides}")

        if ordre not in ["asc", "desc"]:
            raise ValueError(f"Ordre de tri invalide: '{ordre}'. Valeurs acceptées : ['asc', 'desc']")

        # 3. Extraction des filtres
        filtres = {
            "annee": params.get("annee"),
            "serveur": params.get("serveur"),
            "jeu": params.get("jeu"),
            "file": params.get("file"),
        }

        # 4. Appel au repositories
        data, total = PartiesRepository.get_parties(limit, offset, tri, ordre, filtres)

        return {
            "data": data,
            "total": total,
            "limit": limit,
            "offset": offset
        }
