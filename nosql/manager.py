import redis


class PrefijosKeys:
    def __init__(self):
        self.correosPrefijo = "correos::"
        self.usuariosPrefijo = "usuarios::"
        self.correosSospechososPrefijo = "correos_sos::"
        self.correosSospechososHashPrefijo = "correosHash_sos"


class RedisManager:
    def __init__(self, host, port, password, db, pool=False):

        # si tenemos muchos nombres,
        # mejor ponerlo en una class?
        self.prefijos = PrefijosKeys()

        try:

            if pool == False:
                self.rediscliente = redis.Redis(
                    host=host, port=port, password=password, db=db)
            else:
                # pool
                redis_pool = redis.ConnectionPool(
                    host=host, port=port, db=db, password=password)
                self.rediscliente = redis.Redis(connection_pool=redis_pool)

        except redis.RedisError as error:
            print("Redis error {0}".format(error))

    def comprobarusuario(self, nombreusuario):
        print(self.rediscliente.exists(
            self.prefijos.usuariosPrefijo + nombreusuario))

        try:
            if self.rediscliente.exists(self.prefijos.usuariosPrefijo + nombreusuario) >= 1:
                return True
            return False

        except redis.RedisError as error:
            print("Redis error {0}".format(error))
            raise Exception("Redis error {0}".format(error))

    def comprobarcorreo(self, email):
        try:
            ok = self.rediscliente.exists(
                self.prefijos.correosPrefijo + email)
            if ok >= 1:
                return True

            return False
        except redis.RedisError as error:
            print("Redis error {0}".format(error))
            raise Exception("Redis error {0}".format(error))

    def añadirCorreoEmail(self, email):
        try:
            # mejor con hash
            ok = self.rediscliente.set(
                self.prefijos.correosPrefijo + email, email)
            return ok

        except redis.RedisError as error:
            print("Redis error {0}".format(error))
            raise Exception("Redis error {0}".format(error))
        
    def anadirlistasospechosos(self, ip, email, nombre):
        try:
            # mejor con hash
            ok = self.rediscliente.set(
                self.prefijos.correosSospechososPrefijo + email, email)
            
            #
            
            ok = self.rediscliente.hset(
                self.prefijos.correosSospechososHashPrefijo, "ip", ip
            )
            return ok

        except redis.RedisError as error:
            print("Redis error {0}".format(error))
            raise Exception("Redis error {0}".format(error))
            
        

    def redisClose(self):
        self.rediscliente.close()
        print("Redis destroyed")


redisman = RedisManager(host='redis-19111.c55.eu-central-1-1.ec2.cloud.redislabs.com', port=19111,
                        password="NNXYsaSfer3od5xZRqlApthvppdW9Y4f", db=0)
