"""
Sistema de Gestión de Citas para Clínica/Consultorio
Análisis de Sistemas II — UMG, Sede Puerto Barrios

Aplicación Flask monolítica con arquitectura en tres capas:
    navegador (Jinja2)  →  rutas/ + servicios/ (Flask)  →  models/ (MongoDB vía PyMongo)
"""

import logging
import time

from flask import Flask, g, jsonify, render_template, request, session

import models as db
from config import SECRET_KEY_DESARROLLO, Config
from rutas.auth import auth_bp
from rutas.citas import citas_bp
from rutas.doctores import doctores_bp
from rutas.pacientes import pacientes_bp
from rutas.reportes import reportes_bp
from rutas.bitacora import bitacora_bp
from rutas.perfil import perfil_bp
from rutas.seguridad import csrf_token, proteger_csrf, validar_sesion
from servicios.agenda import dias_texto
from servicios.graficos import COLORES_ESTADO
from servicios.presentacion import edad, fecha_corta, fecha_larga, hoy_texto, relativa


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="plantillas", static_folder="estaticos")
    app.config.from_object(config_class)

    # En producción la clave de sesión debe definirse por variable de entorno
    if app.config["APP_ENV"] == "produccion" and app.config["SECRET_KEY"] == SECRET_KEY_DESARROLLO:
        raise RuntimeError("Define la variable de entorno SECRET_KEY antes de ejecutar en producción.")

    logging.basicConfig(level=app.config["LOG_LEVEL"], format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    # --- Capa de datos: MongoDB si está disponible, memoria como respaldo ---
    db.inicializar(app.config)
    if app.config["SEMBRAR_DEMO"]:
        db.sembrar_datos_demo()

    # --- Blueprints (lógica de negocio por módulo) ---
    for blueprint in (auth_bp, citas_bp, doctores_bp, pacientes_bp, reportes_bp, perfil_bp, bitacora_bp):
        app.register_blueprint(blueprint)

    # --- Seguridad ---
    app.before_request(proteger_csrf)
    app.before_request(validar_sesion)

    @app.before_request
    def _inicio_peticion():
        g.inicio = time.perf_counter()

    @app.after_request
    def cabeceras_seguridad(respuesta):
        duracion = (time.perf_counter() - g.get("inicio", time.perf_counter())) * 1000
        respuesta.headers["X-Response-Time"] = f"{duracion:.0f}ms"
        if duracion > app.config["PETICION_LENTA_MS"] and request.endpoint != "static":
            app.logger.warning("Petición lenta: %s %s tardó %.0f ms", request.method, request.path, duracion)
        respuesta.headers["X-Content-Type-Options"] = "nosniff"
        respuesta.headers["X-Frame-Options"] = "SAMEORIGIN"
        respuesta.headers["Referrer-Policy"] = "same-origin"
        if "usuario_id" in session:  # evita ver datos clínicos con el botón "atrás" tras cerrar sesión
            respuesta.headers["Cache-Control"] = "no-store"
        return respuesta

    # --- Estado del servicio (para monitoreo o balanceadores; no expone datos) ---
    @app.route("/salud")
    def salud():
        try:
            db.repo().contar("especialidades")
            estado, codigo = "ok", 200
        except Exception:  # base de datos caída
            estado, codigo = "degradado", 503
        return jsonify(estado=estado, almacenamiento=db.info_almacenamiento()["modo"], version=app.config["VERSION"]), codigo

    # --- Plantillas ---
    app.jinja_env.globals["csrf_token"] = csrf_token
    app.jinja_env.globals["COLORES_ESTADO"] = COLORES_ESTADO
    app.jinja_env.filters.update(
        dias_texto=dias_texto, fecha_corta=fecha_corta, fecha_larga=fecha_larga, relativa=relativa, edad=edad,
    )

    @app.context_processor
    def contexto_global():
        return {"almacenamiento": db.info_almacenamiento(), "nombre_clinica": app.config["NOMBRE_CLINICA"],
                "version_assets": app.config["VERSION"], "hoy": hoy_texto()}

    # --- Páginas de error amigables ---
    errores = {
        400: ("Solicitud no válida", "El formulario expiró o no es válido. Vuelve a intentarlo desde la página anterior.", "bi-shield-exclamation"),
        403: ("Acceso restringido", "No tienes permiso para ver esta sección. La información clínica solo está disponible para el administrador y el doctor asignado.", "bi-lock-fill"),
        404: ("Página no encontrada", "La dirección que buscas no existe o fue movida.", "bi-compass"),
        500: ("Algo salió mal", "Ocurrió un error inesperado en el servidor. Intenta nuevamente en unos momentos.", "bi-bug"),
    }

    def _manejar(codigo):
        titulo, mensaje, icono = errores[codigo]

        def manejador(_error):
            return render_template("error.html", codigo=codigo, titulo=titulo, mensaje=mensaje, icono=icono), codigo
        return manejador

    for codigo in errores:
        app.register_error_handler(codigo, _manejar(codigo))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])
