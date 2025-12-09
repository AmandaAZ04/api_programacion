def resumen_todos_por_usuario(todos_json):
    """
    Recibe una lista de TODOS en formato JSON y devuelve un resumen
    por cada usuario:
    { userId: { total: X, completados: Y } }
    """
    resumen = {}

    for t in todos_json:
        uid = t["userId"]

        if uid not in resumen:
            resumen[uid] = {
                "total": 0,
                "completados": 0
            }

        resumen[uid]["total"] += 1

        if t.get("completed"):
            resumen[uid]["completados"] += 1

    return resumen