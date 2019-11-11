"""
REGISTRO Y LOGIN

"""

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session

from flask_bootstrap import Bootstrap
from formularios.forms import FormularioLogin
from formularios.forms import FormularioRegistro
from formularios.forms import comprobarRedisLogin
from formularios.forms import añadirCorreoEmail

import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "HOOLA"
bootstrap = Bootstrap(app)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET"])
def login():
    templatelogin = FormularioLogin()
    templateregistro = FormularioRegistro()
    return render_template("login.html", templatelogin=templatelogin, templateregistro=templateregistro)


@app.route("/login", methods=["POST"])
def loginusuario():
    # jaskjasd@gmail.com

    if request.form["opcion"] == "loginusuario":

        templatelogin = FormularioLogin(request.form)
        if templatelogin.validate() == True:

            if comprobarRedisLogin(templatelogin, templatelogin.emailLogin) == True:
                # el email existe
                # comprobamos el password que sea correcto.
                # el cliente con el email tiene un valid device cookie ?

                pass
            else:
                # el email no existe
                # mostramos el panel de registro
                templateregistro = FormularioRegistro()
                templateregistro.emailRegistro = templatelogin.emailLogin

                return render_template("login.html", templatelogin=templatelogin, templateregistro=templateregistro,
                                       verregistro=True, emailanterior=templatelogin.emailLogin.data)

            print(templatelogin.data["email"])
            print("Login correcto")
        else:
            print("Login incorrecto")
            templateregistro = FormularioRegistro()

            return render_template("login.html", templatelogin=templatelogin, templateregistro=templateregistro)

    elif request.form["opcion"] == "registrousuario":
        templateregistro = FormularioRegistro(request.form)

        if (templateregistro.validate() == True):
            if comprobarRedisLogin(templateregistro, templateregistro.emailRegistro) == True:
                # el usuario existe
                # mostrar el formulario de login ?
                pass
            else:
                # el usuario no existe
                # añadirlo
                terminar = False
                while(terminar == False):
                    if añadirCorreoEmail(templateregistro.emailRegistro) == True:
                        terminar = True
                        # esperar .. pero es bloqueante ?
                        time.sleep(1)


@app.route("/registro", methods=["POST"])
def registrousuario():
    print("registrousuario")

    return render_template("login.html")


@app.route("/cookie-policy", methods=["GET"])
def showcookiepolicy():
    return render_template("cookie-policy.html")


if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
