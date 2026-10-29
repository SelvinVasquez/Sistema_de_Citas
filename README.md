# 🏥 Clínica Vitalis — Sistema de Gestión de Citas

Proyecto del curso **Análisis de Sistemas II** · Universidad Mariano Gálvez de Guatemala, Sede Puerto Barrios
Catedrático: Ing. Pablo Menjivar · Estudiante: Selvin Vásquez

Aplicación web para gestionar el agendamiento de citas médicas, el expediente clínico básico de los pacientes y la agenda de cada doctor/especialista. Construida con **Python + Flask + Jinja2 + MongoDB (PyMongo)**, tal como se definió en la documentación del proyecto.

---

## 🚀 Inicio rápido

**Opción 1 — doble clic:** ejecuta `iniciar.bat` (crea el entorno, instala lo necesario y abre el navegador).

**Opción 2 — manual (PowerShell):**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Abre <http://127.0.0.1:5000>. El sistema trae **datos de demostración** (5 doctores, 6 pacientes y 19 citas) para poder presentarlo desde el primer arranque. Tampoco necesita internet: Bootstrap, los iconos y la tipografía están incluidos en `estaticos/vendor/`.

### Cuentas de demostración

En la pantalla de inicio hay botones de acceso rápido para cada rol.

| Rol | Correo | Contraseña |
|---|---|---|
| Administrador / Recepción | admin@clinica.com | admin123 |
| Doctor | ana.marroquin@clinica.com | doctor123 |
| Paciente | mario.gomez@correo.com | paciente123 |

## 🍃 MongoDB

El sistema se conecta a MongoDB automáticamente al arrancar (`mongodb://localhost:27017`, base `clinica_citas`).

1. Instala **MongoDB Community Server** y deja el servicio encendido.
2. `pip install -r requirements.txt` (incluye PyMongo).
3. Ejecuta `python app.py`. En la barra lateral aparecerá **«MongoDB conectado»**.

Si MongoDB no está disponible, el sistema **no se cae**: usa un almacenamiento en memoria y lo indica en la barra lateral («Modo demostración»). Así siempre se puede presentar. Al conectarse por primera vez crea las colecciones con validación de esquema (`$jsonSchema`), índices únicos y los datos de demostración.

Variables de entorno opcionales: `MONGO_URI`, `MONGO_DB`, `SEMBRAR_DEMO=0` (no cargar datos de ejemplo), `MODO_DEMO=0` (ocultar los accesos rápidos del login), `USAR_MEMORIA=1` (forzar modo memoria), `SECRET_KEY`.

---

## ✨ Funciones adicionales (más allá de la documentación)

| Función | Qué aporta | Dónde |
|---|---|---|
| 📅 **Calendario mensual** | Vista de todo el mes con las citas por día y color según estado; el admin filtra por doctor y cada rol ve solo lo suyo | `/citas/calendario` |
| 🧾 **Comprobante imprimible** | Cada cita genera un comprobante con código `CIT-00001`, listo para imprimir o guardar como PDF | `/citas/<id>/comprobante` |
| 👤 **Mi perfil** | Cada usuario edita sus datos y cambia su contraseña (pide la actual, con indicador de fortaleza) | `/perfil/` |
| 🕵️ **Bitácora de actividad** | Registro de quién hizo qué y cuándo (sesiones, citas, altas, expedientes consultados, intentos fallidos); filtrable y exportable a CSV. Solo administrador | `/bitacora/` |
| 🛡️ **Bloqueo por intentos fallidos** | 5 contraseñas incorrectas seguidas bloquean ese correo 5 minutos (configurable con `LOGIN_MAX_INTENTOS` y `LOGIN_BLOQUEO_SEG`) | `servicios/limitador.py` |
| 🔒 **Sesión siempre vigente** | Si el administrador desactiva una cuenta, su sesión abierta deja de funcionar al instante | `rutas/seguridad.py` |
| ⚡ **Próximo horario libre** | Cada doctor muestra su primer hueco disponible y el botón de agendar lo abre con esa fecha | `servicios/agenda.py` |
| 🌙 **Modo oscuro** | Botón en la barra superior; se recuerda en el navegador | `estaticos/css/style.css` |

---

## ✅ Cumplimiento de los requerimientos documentados

### Funcionales

| ID | Requerimiento | Dónde está |
|---|---|---|
| RF01 | Registro e inicio de sesión con roles | `rutas/auth.py` (login, registro de pacientes), `rutas/seguridad.py` |
| RF02 | Gestionar doctores (crear, editar, inactivar; especialidad y horario) | `rutas/doctores.py` |
| RF03 | Agendar cita: doctor, especialidad, fecha y hora disponible | `rutas/citas.py`, `servicios/agenda.py`, `estaticos/js/agenda.js` |
| RF04 | Reprogramar cita | `rutas/citas.py` → `reprogramar` |
| RF05 | Cancelar cita con motivo | `rutas/citas.py` → `cancelar` |
| RF06 | No permitir dos citas en el mismo horario de un doctor | `models/cita.py` (validación + bloqueo), `servicios/agenda.py`, índice único parcial en MongoDB |
| RF07 | Expediente clínico básico (motivo, notas, historial) | `rutas/pacientes.py` → `expediente` |
| RF08 | Listado de citas filtrable por día, doctor y paciente | `rutas/citas.py` → `listar` |
| RF09 | Reportes de atendidas / canceladas / pendientes por rango de fechas | `rutas/reportes.py` (+ gráficos y exportación CSV) |
| RF10 | Recordatorios internos de citas próximas al iniciar sesión | aviso al ingresar + paneles de inicio por rol |
| RF11 | Expedientes solo para el doctor asignado y el administrador | `rutas/pacientes.py` → `_validar_acceso_expediente` |
| RF12 | Administrador da de alta, edita y desactiva cuentas | `rutas/auth.py` → `/usuarios` |

### No funcionales

| ID | Cómo se cumple |
|---|---|
| RNF01 Usabilidad | Agendar en 4 pasos guiados con horarios en botones y resumen en vivo |
| RNF02 Disponibilidad | Modo de respaldo en memoria si MongoDB no responde |
| RNF03 Seguridad | Contraseñas cifradas (`werkzeug.security`), permisos por rol, protección CSRF en todos los formularios, cookies `HttpOnly`/`SameSite`, cabeceras de seguridad, sin caché de datos clínicos, bloqueo temporal tras intentos fallidos, cierre inmediato de sesiones de cuentas desactivadas y bitácora de actividad |
| RNF05 Escalabilidad | Doctores, especialidades y horarios son datos configurables; el repositorio de datos es intercambiable |
| RNF06 Portabilidad | Diseño responsivo (menú lateral desplegable en móvil) |
| RNF07 Mantenibilidad | Código por capas, SOLID y Clean Code (ver abajo) |
| RNF08 Confidencialidad | Acceso clínico restringido (RF11) y datos clínicos sin caché del navegador |
| RNF09 Consistencia de datos | Validación de esquema `$jsonSchema`, índices únicos (id, correo, horario por doctor) y relaciones por referencia |

---

## 🧱 Arquitectura

Aplicación monolítica en **tres capas** (cliente–servidor): navegador → servidor Flask → MongoDB.

```
app.py                  Fábrica de la aplicación y registro de blueprints
config.py               Configuración centralizada
models/                 Capa de datos
  repositorio.py          Contrato + RepositorioMongo (PyMongo) y RepositorioMemoria
  conexion.py             Elige el repositorio al arrancar
  usuario.py · doctor.py · paciente.py · cita.py · expediente.py · especialidad.py · bitacora.py
  semilla.py              Datos de demostración
servicios/              Reglas de negocio reutilizables
  agenda.py               Disponibilidad y validación de horarios
  validaciones.py         Validación de formularios
  altas.py · graficos.py · presentacion.py
  auditoria.py            Escribe en la bitácora con el usuario de la sesión
  limitador.py            Límite de intentos de inicio de sesión
rutas/                  Blueprints (controladores)
  auth.py · citas.py · doctores.py · pacientes.py · reportes.py · perfil.py · bitacora.py · seguridad.py
plantillas/             Vistas Jinja2 (+ _macros.html con componentes reutilizables)
estaticos/              CSS, JavaScript y recursos locales (vendor/)
pruebas/                Plan de pruebas automatizado
```

**Principios SOLID aplicados**

- **S** — cada módulo tiene una responsabilidad: rutas reciben peticiones, servicios aplican reglas, modelos guardan datos.
- **O** — nuevas formas de almacenamiento se agregan creando otro `Repositorio`, sin tocar las rutas.
- **L** — `RepositorioMongo` y `RepositorioMemoria` son sustituibles entre sí (el plan de pruebas pasa idéntico con ambos).
- **I** — el contrato `Repositorio` expone solo las operaciones necesarias.
- **D** — los modelos dependen de la abstracción `Repositorio`, no de PyMongo.

### Colecciones de MongoDB (modelo entidad-relación)

`especialidades` 1—N `doctores` · `doctores` 1—N `citas` · `pacientes` 1—N `citas` · `pacientes` 1—1 `expedientes` · `usuarios` 1—1 `doctores` / `pacientes`. Más la colección `bitacora` (auditoría de actividad) y la colección técnica `contadores` para los identificadores autoincrementales.

---

## 🧪 Plan de pruebas

```powershell
python -m unittest discover -s pruebas -v
```

61 pruebas automatizadas que cubren RF01–RF12 (inicio de sesión, registro, agendamiento, choque de horarios, reprogramación, cancelación, permisos por rol, expedientes, reportes y exportación), las funciones adicionales (bloqueo por intentos, perfil, bitácora, calendario, comprobante y próximo horario libre) y recorren todas las pantallas de cada rol. Se ejecutaron con ambos almacenamientos (memoria y MongoDB simulado) con resultado exitoso.

---

## 📁 Nota sobre `_respaldo_original/`

Contiene la versión anterior del prototipo (con `data_store.py` en memoria) por si se desea comparar. Se puede eliminar sin afectar al sistema.
