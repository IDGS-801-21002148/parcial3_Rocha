import os
import csv
import datetime
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from config import DevelopmentConfig
from models import db, User, Cliente, Pizzas
from forms import LoginForm, RegisterForm, ClienteForm, PizzaForm, ConsultaVentasForm

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        # Mensajes específicos de error
        if not user:
            flash("El usuario no existe.", "error")
        elif not user.check_password(password):
            flash("Contraseña incorrecta.", "error")
        else:
            login_user(user)
            return redirect(url_for("pizzas"))

    return render_template("index.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("El usuario ya existe", "error")
            return redirect(url_for("register"))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Usuario registrado correctamente. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("index"))

    return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/pizzas", methods=["GET", "POST"])
@login_required
def pizzas():
    cliente_form = ClienteForm()
    pizza_form = PizzaForm()
    consulta_ventas_form = ConsultaVentasForm()
    pedidos = session.get("pedidos", [])

    if request.method == "POST":
        if cliente_form.validate_on_submit() and pizza_form.validate_on_submit():
            cliente_data = {
                "nombre": cliente_form.nombre.data,
                "direccion": cliente_form.direccion.data,
                "telefono": cliente_form.telefono.data,
                "fecha_pedido": cliente_form.fecha_pedido.data.strftime('%Y-%m-%d')
            }
            session["cliente_data"] = cliente_data

            tamaño = pizza_form.tamaño.data
            ingredientes = ", ".join(pizza_form.ingredientes.data)
            cantidad = pizza_form.cantidad.data

            precio_tamaño = {"Chica": 40, "Mediana": 80, "Grande": 120}
            precio_ingredientes = 10 * len(pizza_form.ingredientes.data)
            subtotal = (precio_tamaño[tamaño] + precio_ingredientes) * cantidad

            pedido = {
                "tamaño": tamaño,
                "ingredientes": ingredientes,
                "cantidad": cantidad,
                "subtotal": subtotal
            }
            pedidos.append(pedido)
            session["pedidos"] = pedidos

            flash("Pizza agregada a la lista de pedidos", "success")
            return redirect(url_for("pizzas"))

    ventas_dia = []
    total_ventas = 0
    total_pedidos = 0
    if os.path.exists("ventas.txt"):
        with open("ventas.txt", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                ventas_dia.append(row)
                total_ventas += float(row[1])
                total_pedidos += 1

    return render_template(
        "pizzas.html",
        cliente_form=cliente_form,
        pizza_form=pizza_form,
        pedidos=pedidos,
        ventas_dia=ventas_dia,
        total_ventas=total_ventas,
        total_pedidos=total_pedidos,
        consulta_ventas_form=consulta_ventas_form,
    )

@app.route("/terminar_pedido", methods=["POST"])
@login_required
def terminar_pedido():
    pedidos = session.get("pedidos", [])
    if not pedidos:
        flash("No hay pedidos para terminar", "warning")
        return redirect(url_for("pizzas"))

    total = sum(pedido["subtotal"] for pedido in pedidos)
    cliente_data = session.pop("cliente_data", {})

    cliente = Cliente(
        nombreCompleto=cliente_data.get("nombre"),
        direccion=cliente_data.get("direccion"),
        telefono=cliente_data.get("telefono"),
        fechaPedido=datetime.datetime.strptime(cliente_data.get("fecha_pedido"), "%Y-%m-%d"),
        total=total
    )
    db.session.add(cliente)

    for pedido in pedidos:
        pizza = Pizzas(
            tamaño=pedido["tamaño"],
            ingredientes=pedido["ingredientes"],
            cantidadPizzas=pedido["cantidad"],
            subTotal=pedido["subtotal"]
        )
        db.session.add(pizza)
    db.session.commit()

    with open("ventas.txt", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([cliente.nombreCompleto, total, cliente.fechaPedido.strftime("%Y-%m-%d")])

    session.pop("pedidos", None)
    flash(f"Pedido terminado con éxito. Total a pagar: ${total}", "success")
    return redirect(url_for("pizzas"))

@app.route("/quitar_pizza/<int:pizza_id>", methods=["POST"])
@login_required
def quitar_pizza(pizza_id):
    pedidos = session.get("pedidos", [])
    if pedidos:
        pedidos.pop(pizza_id)
        session["pedidos"] = pedidos
        flash("Pizza quitada de la lista de pedidos", "warning")
    return redirect(url_for("pizzas"))

@app.route("/consultar_ventas", methods=["GET", "POST"])
@login_required
def consultar_ventas():
    consulta_ventas_form = ConsultaVentasForm()
    total_ventas = 0
    total_pedidos = 0
    ventas_dia = []

    if consulta_ventas_form.validate_on_submit():
        periodo = consulta_ventas_form.periodo.data
        fecha = consulta_ventas_form.fecha.data

        if periodo == "dia":
            fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")
            with open("ventas.txt", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[2] == fecha_hoy:
                        ventas_dia.append(row)
                        total_ventas += float(row[1])
                        total_pedidos += 1

        elif periodo == "mes":
            fecha_actual = datetime.datetime.now()
            año = fecha_actual.strftime("%Y")
            mes = fecha_actual.strftime("%m")
            fecha_inicio = f"{año}-{mes}-01"
            fecha_fin = f"{año}-{mes}-31"

            with open("ventas.txt", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if fecha_inicio <= row[2] <= fecha_fin:
                        ventas_dia.append(row)
                        total_ventas += float(row[1])
                        total_pedidos += 1

        elif periodo == "ninguno" and fecha:
            with open("ventas.txt", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[2] == fecha:
                        ventas_dia.append(row)
                        total_ventas += float(row[1])
                        total_pedidos += 1

    return render_template(
        "consultar_ventas.html",
        consulta_ventas_form=consulta_ventas_form,
        total_ventas=total_ventas,
        total_pedidos=total_pedidos,
        ventas_dia=ventas_dia,
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)