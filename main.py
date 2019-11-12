"""
REGISTRO Y LOGIN

"""

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import abort

from flask_bootstrap import Bootstrap
from formularios.forms import FormularioLogin
from formularios.forms import FormularioRegistro
# from formularios.forms import comprobarRedisLogin
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

    if ("emailLogin" and "passwordLogin" in session) == True:
        # comprobar que este correcto
        # si es correcto
            # return redirect(url_for("profile"))
        # sino
        pass

    templatelogin = FormularioLogin()
    templateregistro = FormularioRegistro()

    context = {
        "templatelogin": templatelogin,
        "templateregistro": templateregistro,
        "emailanterior": "",
        "intentos": 1,
        "verloginmodal": True,
        "verregistromodal": False
    }

    # return render_template("login.html", templatelogin=templatelogin, templateregistro=templateregistro, intentos=1)
    return render_template("login.html", datos=context)


@app.route("/login", methods=["GET"])
def mostrarlogin_modal():
    templatelogin = FormularioLogin()
    templateregistro = FormularioRegistro()

    context = {
        "templatelogin": templatelogin,
        "templateregistro": templateregistro,
        "emailanterior": "",
        "intentos": 1,
        "verloginmodal": True,
        "verregistromodal": False
    }

    # return render_template("login.html", templatelogin=templatelogin, templateregistro=templateregistro, intentos=1,
    #                        verloginmodal=True, verregistroModal=False
    #                        )
    return render_template("login.html", datos=context)


@app.route("/login", methods=["GET"])
def mostrarregistro_modal():

    templatelogin = FormularioLogin()
    templateregistro = FormularioRegistro()

    context = {
        "templatelogin": templatelogin,
        "templateregistro": templateregistro,
        "emailanterior": "",
        "intentos": 1,
        "verloginmodal": False,
        "verregistromodal": True
    }

    # return render_template("login.html", templatelogin=templatelogin, templateregistro=templateregistro, intentos=1, verregistro=True)
    return render_template("login.html", datos=context)


@app.route("/login", methods=["POST"])
def loginusuario():
    # jaskjasd@gmail.com
    # borrar cookie de session
    # session.clear()
    if request.form["emailLoginhidden"] != "":
        # uuu posible spam bot
        # TODO: ponerlo en listaado de sospechosos
        pass

    if request.form["opcion"] == "loginusuario":

        templatelogin = FormularioLogin(request.form)
        if templatelogin.validate() == True:

            if templatelogin.comprobarRedisLogin(templatelogin, templatelogin.emailLogin) == True:
                # el email existe
                # comprobamos el password que sea correcto.
                # el cliente con el email tiene un valid device cookie ?
                if templatelogin.comprobarEmailPasswordMysql(templatelogin, templatelogin.emailLogin, templatelogin.passwordLogin) == True:

                    # TODO: datos = templatelogin.sacardatos(emailLogin, passwordLogin)

                    session["email"] = request.form["emailLogin"]
                    session["password"] = request.form["passwordLogin"]
                    # session["nombre"] = datos[0][2]

                    return redirect(url_for("profile"))

                else:
                    # intentos 3 ?
                    try:
                        intentos = int(request.form["intentos"])
                    except ValueError:
                        raise Exception("valor no valido")

                    intentos += 1
                    print("intentos=".format(intentos))

                    if intentos > 3:
                        # TODO: meter en la db de sospechosos.
                        # captcha despues de 
                        return redirect(url_for("login"))
                        # return abort(404)
                    else:
                        templateregistro = FormularioRegistro()

                        context = {
                            "templatelogin": templatelogin,
                            "templateregistro": templateregistro,
                            "emailanterior": templatelogin.emailLogin.data,
                            "intentos": intentos,
                            "verloginmodal": False,
                            "verregistromodal": True,
                        }

                        return render_template("login.html", datos=context)

                        # return render_template("login.html", templatelogin=templatelogin, templateregistro=templateregistro,
                        #                        verregistro=True, emailanterior=templatelogin.emailLogin.data, intentos=intentos)

            else:
                # el email no existe
                # mostramos el panel de registro
                templateregistro = FormularioRegistro()
                templateregistro.emailRegistro = templatelogin.emailLogin

                try:
                    intentos = int(request.form["intentos"])
                except ValueError:
                    raise Exception("valor no valido")

                intentos += 1

                context = {
                    "templatelogin": templatelogin,
                    "templateregistro": templateregistro,
                    "emailanterior": templatelogin.emailLogin.data,
                    "intentos": intentos,
                    "verloginmodal": False,
                    "verregistromodal": True,
                }
                return render_template("login.html", datos=context)

                # return render_template("login.html", templatelogin=templatelogin, templateregistro=templateregistro,
                #                        verregistro=True, emailanterior=templatelogin.emailLogin.data)

            print(templatelogin.data["email"])
            print("Login correcto")
        else:
            print("Login incorrecto")
            templateregistro = FormularioRegistro()

            context = {
                "templatelogin": templatelogin,
                "templateregistro": templateregistro,
                "emailanterior": templatelogin.emailLogin.data,
                "intentos": 1,
                "verloginmodal": True,
                "verregistromodal": False,
            }
            return render_template("login.html", datos=context)

            # return render_template("login.html", templatelogin=templatelogin, templateregistro=templateregistro)


@app.route("/registro", methods=["POST"])
def registrousuario():
    print("registrousuario")

    if request.form["emailRegistrohidden"] != "":
        # todo: sopechoso
        ip = request.remote_addr
        # from nosql.manager import redisman.anadirlistasospechosos(request.remote_addr,
        #                                                           request.form["emailRegistro"],
        #                                                           request.form["nombreRegistro"]
        #                                                           )
        pass
    
    # PARA REGISTRO 

    if request.form["opcion"] == "registrousuario":
        templateregistro = FormularioRegistro(request.form)
        templatelogin = FormularioLogin()

        if (templateregistro.validate() == True):
            if templateregistro.comprobarRedisLogin(templateregistro, templateregistro.emailRegistro) == True:
                # el usuario existe
                # mostrar el formulario de login ?

                templatelogin = FormularioLogin()
                templatelogin.emailLogin = templateregistro.emailRegistro

                return render_template("login.html", templatelogin=templatelogin, templateregistro=templateregistro,
                                       verregistro=False, verlogin=True, emailanterior=templateregistro.emailRegistro.data)

                pass
            else:
                # el usuario no existe
                # añadirlo
                # TODO bloquear que no pueda pulsar o salir del formulario

                ok = templateregistro.comprobarDBCorreoRegistro(
                    templateregistro, templateregistro.emailRegistro)
                if ok == True:
                    respuesta = templateregistro.anadirCorreoUsuario(templateregistro.emailRegistro,
                                                                     templateregistro.passwordRegistro,
                                                                     templateregistro.nombreRegistro
                                                                     )
                    if respuesta == True:
                        # mandarlo a login para que valide que es usuario correcto
                        # en vez de mandarlo directo al profile.
                        return redirect(url_for("login"))

                    else:
                        return redirect(url_for("registro"))

                else:
                    return redirect(url_for("login"))

                terminar = False
                while(terminar == False):
                    if añadirCorreoEmail(templateregistro.emailRegistro) == True:
                        terminar = True
                        # esperar .. pero es bloqueante ?
                        time.sleep(1)

        return render_template("login.html", templatelogin=templatelogin, templateregistro=templateregistro)


@app.route("/profile", methods=["GET"])
def profile():
    print("dentro")
    if ("emailLogin" and "passwordLogin" in session) == False:
        # todo: añadir usuario sospechosos
        session.clear()
        return redirect(url_for("mostrarregistro_modal"))

    else:
        email = session["emailLogin"]
        password = session["passwordLogin"]
        nombre = session["nombre"]
        session["mostrarlogin"] = False

        return render_template("profile.html", nombre=nombre, email=email)


@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for("login"))


@app.route("/registro", methods=["GET"])
def redirect_registrousuario():
    print("registrousuario")

    return redirect(url_for("login"))


@app.route("/cookie-policy", methods=["GET"])
def showcookiepolicy():
    return render_template("cookie-policy.html")


if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
