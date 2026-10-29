"""Punto de entrada para servidores de producción (WSGI).

Ejemplos:
    waitress-serve --listen=0.0.0.0:8000 wsgi:app      (Windows o Linux)
    gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app             (Linux)

Antes de ejecutar: APP_ENV=produccion y SECRET_KEY=<clave larga y aleatoria>.
"""

from app import app  # noqa: F401
