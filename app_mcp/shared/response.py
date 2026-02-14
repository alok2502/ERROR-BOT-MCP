def success_response(message: str, data: dict):
    return {
        "status": "success",
        "message": message,
        "data": data,
    }


def error_response(message: str):
    return {
        "status": "error",
        "message": message,
    }
