@echo off
REM Inicia el Sistema de Citas Clinica Vitalis con un doble clic.
cd /d "%~dp0"
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)
call venv\Scripts\activate
echo Instalando dependencias...
pip install -r requirements.txt -q
echo.
echo Sistema listo en http://127.0.0.1:5000  (Ctrl+C para detener)
start "" http://127.0.0.1:5000
python app.py
