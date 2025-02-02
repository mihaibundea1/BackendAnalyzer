from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity
)
from extensions import jwt
from blacklist import blacklist  # presupunând că blacklist-ul este definit într-un modul separat
from app.services import UserService  # Asigură-te că calea este corectă

auth_routes = Blueprint("auth", __name__)

# Exemplu simplu de "bază de date" a utilizatorilor
users = {"user_exemplu": "parola_exemplu"}

@auth_bp.route("/login", methods=["POST"])
def login():
    # Presupunem că login-ul se face pe baza email-ului
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email or not password:
        return jsonify({"msg": "Email și parola sunt necesare"}), 400

    # Obținem utilizatorul din baza de date folosind serviciul
    user = UserService.get_user_by_email(email)
    if not user:
        return jsonify({"msg": "Utilizatorul nu a fost găsit"}), 404

    # Verificăm parola folosind check_password_hash
    if not check_password_hash(user.password_hash, password):
        return jsonify({"msg": "Datele de autentificare sunt invalide"}), 401

    # Opțional: aici poți implementa verificarea MFA (de exemplu, cu pyotp) dacă este necesar

    # Crearea token-urilor de acces și refresh, folosind, de exemplu, user.id ca identity
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200

@auth_bp.route("/logout_access", methods=["POST"])
@jwt_required()
def logout_access():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify(msg="Access token a fost revocat"), 200

@auth_bp.route("/logout_refresh", methods=["POST"])
@jwt_required(refresh=True)
def logout_refresh():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify(msg="Refresh token a fost revocat"), 200