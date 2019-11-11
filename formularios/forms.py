from wtforms import Form
from wtforms import StringField
from wtforms import TextField
from wtforms import validators
from wtforms import HiddenField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import ValidationError

from wtforms.fields.html5 import EmailField
from mysql.manager import sqlman
from nosql.manager import redisman


# comprobar correo al validarlo
# comprobacion en db nosql si existe el usuario y correo
def comprobarDBCorreoRegistro(form, field: StringField):
    print("comprobar correo => campo {0}".format(field.data))

    ok = sqlman.comprobarEmail(field.data)
    if ok[0] == 0:
        return ok
    elif ok[0] == 1:
        raise ValidationError("Ya existe correo")
    elif ok[0] == 2:
        raise ValidationError("Error {0}".format(ok[1]))


def comprobarDBCorreoLogin(form, field: StringField):
    print("comprobar correo => campo {0}".format(field.data))

    ok = sqlman.comprobarEmailLogin(field.data)
    if ok[0] == True:
        # no ha dado errores
        if ok[1] == None:
            raise ValidationError("No existe el correo")
        # else:
        #     return ok[1]
    elif ok[0] == False:
        # ok[0][1][0][0]
        raise ValidationError("Error {0}".format(ok[1]))


def comprobarRedisLogin(form, field: StringField):
    print("comprobar correo => campo {0}".format(field.data))
    # redireccion
    ok = redisman.comprobarcorreo(field.data)
    return ok

    # if ok == False:
    #     raise ValidationError("No existe correo")


def comprobarExisteUsuario(form, field: StringField):
    print("comprobar usuario => campo {0}".format(field.data))
    # if red.comprobarusuario(field.data) == True:
    #     raise ValidationError("Ya existe Usuario")


def comprobarTodoAlfabeto(form, field: StringField):
    print("comprobar aLF campo {0}".format(field.data))
    # no quiero luchar con regex
    for letra in field.data:
        if letra.isalnum() == False:
            raise ValidationError("Caracteres permitidos entre a y z, 0 y 9")


def añadirCorreoEmail(form, field: EmailField):
    print("comprobar Correo email {0}".format(field.data))
    ok = añadirCorreoEmail(field.data)
    return ok


class FormularioLogin(Form):
    emailLogin = EmailField("email: ", validators=[
        validators.data_required(message="Este campo es requerido"),
        validators.email("Ingrese un email correcto")
        # ,comprobarRedisLogin  # nosql
        # comprobarDBCorreoLogin  # mysql

    ], description="Email")

    emailhidden = HiddenField("email")

    passwordLogin = PasswordField("Password: ", validators=[
        validators.data_required(
            message="Estas obligado a rellenar este campo"),
        validators.length(
            min=4, max=10, message="Clave entre 4 y 10 caracteres")
    ], description="Password")

    confirmPasswordLogin = PasswordField("Repite Password: ", validators=[
        validators.data_required(
            message="Estas obligado a rellenar este campo"),
        validators.equal_to("passwordLogin", "Deben ser iguales")

    ], description="Repite Password")


class FormularioRegistro(Form):
    nombreRegistro = StringField(label="Nombre contacto", validators=[
        validators.required(message="Valor requerido"),
        validators.length(
            min=4, max=10, message="Entre 4 y 10 caracteres de longitud"),
        # validators.any_of("a-Z0-9", "Solo letras y numeros"),
        comprobarTodoAlfabeto

    ], description="Nombre contacto")

    emailRegistro = EmailField("email: ", validators=[
        validators.data_required(message="Este campo es requerido"),
        validators.email("Ingrese un email correcto")

        # ,comprobarDBCorreoRegistro

    ], description="Email")

    passwordRegistro = PasswordField("Password: ", validators=[
        validators.data_required(
            message="Estas obligado a rellenar este campo"),
        validators.length(
            min=4, max=10, message="Clave entre 4 y 10 caracteres")
    ], description="Password")

    confirmPasswordRegistro = PasswordField("Repite Password: ", validators=[
        validators.data_required(
            message="Estas obligado a rellenar este campo"),
        validators.equal_to("passwordRegistro", "Deben ser iguales")

    ], description="Repite Password")

    # aceptoTerminos = BooleanField("Acepto los terminos", validators=[validators.data_required()],
    #                               description="Acepto los terminos")
