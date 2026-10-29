"""Configuración central del sistema (valores sobrescribibles con variables de entorno)."""

import os
from datetime import timedelta


SECRET_KEY_DESARROLLO = "clave-secreta-solo-para-desarrollo"
APP_ENV = os.environ.get("APP_ENV", "desarrollo").lower()  # "desarrollo" | "produccion"


class Config:
    APP_ENV = APP_ENV
    DEBUG = APP_ENV == "desarrollo"
    VERSION = "2.0"  # también invalida la caché de CSS/JS del navegador
    SECRET_KEY = os.environ.get("SECRET_KEY", SECRET_KEY_DESARROLLO)
    HOST = os.environ.get("HOST", "127.0.0.1")
    PORT = int(os.environ.get("PORT", "5000"))

    # --- Rendimiento y operación ---
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(days=7 if APP_ENV == "produccion" else 0)  # caché de archivos estáticos
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
    PETICION_LENTA_MS = int(os.environ.get("PETICION_LENTA_MS", "800"))  # se registra una advertencia si tarda más

    # --- MongoDB (RNF09). Si el servidor no responde se usa el modo memoria. ---
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB = os.environ.get("MONGO_DB", "clinica_citas")
    MONGO_TIMEOUT_MS = int(os.environ.get("MONGO_TIMEOUT_MS", "1500"))
    FORZAR_MEMORIA = os.environ.get("USAR_MEMORIA", "0") == "1"

    # --- Datos de demostración (solo se siembran si la base está vacía) ---
    SEMBRAR_DEMO = os.environ.get("SEMBRAR_DEMO", "1") == "1"

    # --- Sesión (RNF03) ---
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = APP_ENV == "produccion" and os.environ.get("COOKIE_SEGURA", "1") == "1"  # requiere HTTPS
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

    # --- Protección contra adivinar contraseñas: N fallos seguidos bloquean el acceso un tiempo ---
    LOGIN_MAX_INTENTOS = int(os.environ.get("LOGIN_MAX_INTENTOS", "5"))
    LOGIN_BLOQUEO_SEG = int(os.environ.get("LOGIN_BLOQUEO_SEG", "300"))

    NOMBRE_CLINICA = "Clínica Vitalis"
