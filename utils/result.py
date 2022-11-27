def resultat(status, data):
    if isinstance(data, str):
        res = {
            "status": status,
            "message": data
        }
    else:
        res = {
            "status": status,
            "data": data
        }
    return res
