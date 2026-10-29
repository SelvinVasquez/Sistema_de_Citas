# Clínica Vitalis — versión 2.0

## Diseño y experiencia de usuario
- Nuevo diseño "Aurora": menú azul tinta, acentos iris/menta/coral, tarjetas redondeadas, modo oscuro.
- Menú lateral ocultable (botón de la barra superior o Ctrl+B); se recuerda la preferencia.
- Login sin botones de acceso rápido ni credenciales a la vista.
- Avisos y mensaje de bienvenida flotantes (no ocupan espacio en las vistas), se cierran solos.
- Búsqueda rápida Ctrl+K, confirmaciones con ventana propia, bloqueo de envíos dobles.
- Agendar cita: buscador de pacientes con autocompletado.

## Reportes de pacientes
- Nueva página /pacientes/<id>/reporte (lectura) para administrador y TODOS los doctores:
  indicadores, motivo, notas clínicas, historial paginado, exportación CSV e impresión.
- Editar el expediente sigue reservado al administrador y al doctor asignado.
- Cada consulta queda en la bitácora.

## Escalabilidad
- Paginación, búsqueda y conteos en la base de datos (skip/limit, count_documents, $in, $regex).
- Índices de rendimiento en MongoDB; consultas por lote (sin cargar colecciones completas).
- Configuración por entorno (APP_ENV), /salud, cabecera X-Response-Time, wsgi.py y requirements.txt.

## Pruebas
python -m unittest discover -s pruebas   (81 pruebas; también verificadas sobre MongoDB simulado)
