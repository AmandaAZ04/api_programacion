def resumen_todos_por_usuario(todos_json):
    resumen = {}

    for t in todos_json:
        uid = t["userId"]

        if uid not in resumen:
            resumen[uid] = {"total": 0, "completados": 0}

        resumen[uid]["total"] += 1

        if t.get("completed"):
            resumen[uid]["completados"] += 1

    return resumen