import os
# Librerías necesarias de Flask y SQLAlchemy
from flask import Flask, render_template,request, abort,url_for
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Verificar la existencia de la variable de entorno DATABASE_URL
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configurar la sesión para usar el sistema de archivos
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# leer la URL de la base de datos desde la variable de entorno
# y crear una conexión a la base de datos
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("home.html")


#ruta para el registro de empleados
@app.route("/empleados", methods=["GET", "POST"])
def empleados():
    if request.method == "POST":
        nUsuario = request.form.get("nombreUsuario")
        cedula = request.form.get("cedula")
        sexo = request.form.get("sexo")
        edad = request.form.get("edad")
        telefono = request.form.get("telefono")
        cargo = request.form.get("cargo")
        print(nUsuario, cedula, sexo, edad, telefono, cargo)
        # Verificar si el usuario ya existe

        # Verificar si todos los campos están completos
        if not nUsuario or not cedula or not sexo or not edad or not telefono or not cargo:
            data = {
                'icon': 'error',
                'title': 'Error',
                'text': 'Falto llenar algun campo',
                'redirect': 'empleados'
            }
            return render_template("notification.html", data=data)
        
        # Verificar si la cédula ya existe
        if db.execute(text("SELECT * FROM empleados WHERE cedula = :cedula"), {"cedula": cedula}).rowcount > 0:
            data = {
                'icon': 'error',
                'title': 'Error',
                'text': 'La cédula ya existe',
                'redirect': 'empleados'
            }
            return render_template("notification.html", data=data)
        
        #crear el empleado
        db.execute(text("INSERT INTO empleados (nombre, cedula, sexo, edad, telefono, cargo) VALUES (:nUsuario, :cedula, :sexo, :edad, :telefono, :cargo)"),
                   {"nUsuario": nUsuario, "cedula": cedula, "sexo": sexo, "edad": edad, "telefono": telefono, "cargo": cargo})
        db.commit()

        data = {
            'icon': 'success',
            'title': 'Empleado creado',
            'text': 'El empleado fue creado correctamente',
            'redirect': 'empleados'
        }
        return render_template("notification.html", data=data)
    

    # Método GET → cargar lista de empleados
    emp = text("SELECT * FROM empleados")
    empleados = db.execute(emp).fetchall()
    db.commit()

    
    return render_template("empleados.html", empleados=empleados)

#Actualizar empleado
@app.route("/update_empleado/<int:id>", methods=["GET", "POST"])
def update_empleado(id):
    if request.method == "POST":
        nUsuario = request.form.get("nombreUsuario")
        cedula = request.form.get("cedula")
        sexo = request.form.get("sexo")
        edad = request.form.get("edad")
        telefono = request.form.get("telefono")
        cargo = request.form.get("cargo")

        if not nUsuario or not cedula or not sexo or not edad or not telefono or not cargo:
            data = {
                'icon': 'error',
                'title': 'Error',
                'text': 'Falto llenar algun campo',
                'redirect': 'empleados'
            }
            return render_template("notification.html", data=data)

        # Verificar si la cédula ya existe para otro usuario
        if db.execute(text("SELECT * FROM empleados WHERE cedula = :cedula AND id != :id"), {"cedula": cedula, "id": id}).rowcount > 0:
            data = {
                'icon': 'error',
                'title': 'Error',
                'text': 'La cédula ya existe',
                'redirect': 'empleados'
            }
            return render_template("notification.html", data=data)

        # Actualizar el empleado
        db.execute(text("""
            UPDATE empleados 
            SET nombre = :nUsuario, cedula = :cedula, sexo = :sexo, edad = :edad, telefono = :telefono, cargo = :cargo 
            WHERE id = :id
        """), {
            "nUsuario": nUsuario, "cedula": cedula, "sexo": sexo,
            "edad": edad, "telefono": telefono, "cargo": cargo, "id": id
        })
        db.commit()

        data = {
            'icon': 'success',
            'title': 'Empleado actualizado',
            'text': 'El empleado fue actualizado correctamente',
            'redirect': 'empleados'
        }
        return render_template("notification.html", data=data)

    # Recuperar datos del empleado para precargar el formulario
    empleado = db.execute(text("SELECT * FROM empleados WHERE id = :id"), {"id": id}).fetchone()

    if not empleado:
        return "Empleado no encontrado", 404

    return render_template("editar_empleado.html", empleado=empleado)


#visualizar empleado
@app.route("/ver_empleado/<int:id>")
def ver_empleado(id):
    empleado = db.execute(text("SELECT * FROM empleados WHERE id = :id"), {"id": id}).fetchone()

    if not empleado:
        return "Empleado no encontrado", 404

    return render_template("ver_empleado.html", empleado=empleado)

#ruta para eliminar empleado
@app.route("/eliminar_empleado/<int:id>", methods=["POST"])
def eliminar_empleado(id):
    # Verificar si existe
    empleado = db.execute(text("SELECT * FROM empleados WHERE id = :id"), {"id": id}).fetchone()
    if not empleado:
        abort(404)

    # Eliminar empleado
    db.execute(text("DELETE FROM empleados WHERE id = :id"), {"id": id})
    db.commit()

    data = {
        'icon': 'success',
        'title': 'Empleado eliminado',
        'text': 'El empleado fue eliminado correctamente',
        'redirect': 'empleados'
    }
    return render_template("notification.html", data=data)