import pymysql


class ManagerMysql:

    def __init__(self, host, user, password, db, port=3306):

        try:
            self.conexion = pymysql.connect(
                host=host, user=user, password=password, database=db, port=port)
            self.cursor = self.conexion.cursor()
            # self.cursor.execute("select * from leccion7.usuarios")
            # print(self.cursor.fetchall())

        except Exception as error:
            print("Error=> {0}".format(error))
            raise Exception("Error al conectar Mysql error=", error)

    def comprobarEmailLogin(self, email):
        sql = """SELECT email, pass, active FROM leccion7.usuarios where email="{0}"
               """.format(email)
        datos = self.queryinternal(sql)
        return datos

    def anadirCorreoUsuario(self, email, password, nombre):
        sql = """
        INSER INTO leccion7.usuarios (nombre, email, pass)
        VALUES
        ({0}, {1}, {2})
        """.format(nombre, email, password)

        datos = self.queryinternal(sql)
        return datos

    def queryinternal(self, sql):

        try:

            if "SELECT" in sql:
                self.cursor.execute(sql)
                d = self.cursor.fetchall()
                if len(d) <= 0:
                    return True, None
                return True, d

            else:
                self.cursor.execute(sql)
                self.conexion.commit()
                if len(self.cursor.rowcount) <= 0:
                    return True, None
                return True, self.cursor.rowcount

        except pymysql.Error as error:
            print("Error=>{0}={1}".format(sql, error))
            self.conexion.rollback()
            # raise Exception("Error=>{0}={1}".format(sql, error))
            return False, error

    def mysqlClose(self):
        try:
            self.cursor.close()
            self.conexion.close()
            print("Mysql closed")

        except pymysql.Error as error:
            print("mysql error => {0}".format(error))


sqlman = ManagerMysql("localhost", "root", "jose", "leccion7")
