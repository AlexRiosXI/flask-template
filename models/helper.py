from functools import wraps
from flask import request, jsonify
from sierra_madre_core.errors import HTTPError
from sierra_madre_core.schemas import ValidationError


import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

def generate_jwt(user_id: str) -> str:
    payload = {
        "id_user": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "exp": datetime.utcnow() + timedelta(hours=12)  # o el tiempo que quieras
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPError("Token expired", 401)
    except InvalidTokenError:
        raise HTTPError("Invalid token", 401)


def validate_token():
    print(request.cookies)
    token = request.headers.get("Authorization")
    token = token.split(" ")
    if token[0] != "Bearer":
        raise HTTPError("Invalid token", 401)
    token = token[1]
    return decode_jwt(token)["id_user"]

def handle_secure_endpoint(custom_error=400):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                request.id_user = validate_token()
                response = func(*args, **kwargs)
                return response
            except HTTPError as http_ex:
                return jsonify({"error": http_ex.message}), http_ex.status_code
            except ValidationError as e:
                custom_errors = []
                for err in e.errors():
                    field_name = ".".join(str(loc) for loc in err["loc"]) or "input"
                    if err["type"] == "missing":
                        custom_errors.append(f"{field_name} is missing")
                    else:
                        custom_errors.append(f"{field_name}: {err['msg']}")
                error = " ,".join(custom_errors)
                return jsonify({"error": error}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), custom_error
        return wrapper
    return decorator