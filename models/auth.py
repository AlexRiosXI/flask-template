

from sierra_madre_core.requests import handle_endpoint
from sierra_madre_auth.register import register_user
from sierra_madre_auth.login import login_user, refresh_token, get_current_user, logout_user
from sierra_madre_auth.config import get_auth_config
from flask import jsonify, request
import os
from dotenv import load_dotenv
from flask import Blueprint

load_dotenv()

auth_blueprint = Blueprint("auth", __name__)
password_hash_key = os.getenv("JWT_SECRET_KEY")
auth_config = get_auth_config({"password_hash_key": password_hash_key, "autoconfirm_users": True})

@auth_blueprint.route("/register", methods=["POST"])
@handle_endpoint()
def api_register_user():
    return register_user(auth_config)


@auth_blueprint.route("/login", methods=["POST"])
@handle_endpoint()
def api_login_user():
    return login_user(auth_config)

@auth_blueprint.route("/validate-token", methods=["GET"])
@auth_config.handle_secure_endpoint()
def validate_token():
    print("validando token")
    return jsonify({"message": "Token is valid"}), 200

@auth_blueprint.route("/refresh-token", methods=["POST"])
@handle_endpoint()
def api_refresh_token():
    return refresh_token(auth_config)

@auth_blueprint.route("/logout", methods=["POST"])
@handle_endpoint()
def api_logout_user():
    return logout_user()

@auth_blueprint.route("/me", methods=["GET"])
@handle_endpoint()
def api_get_current_user():
    return get_current_user(auth_config)