import os
import sys
import logging
from jmthon.config import Var
from .base import BaseDatabase

Redis = psycopg2 = Database = None
LOGS = logging.getLogger("Jmthon")

if Var.REDIS_URI or Var.REDISHOST:
    try:
        from redis import Redis
    except ImportError:
        LOGS.info("Installing 'redis' for database.")
        os.system(f"{sys.executable} -m pip install -q redis hiredis")
        from redis import Redis

if Redis:
    LOGS.info("Redis successfully imported.")


class RedisDB(BaseDatabase):
    def __init__(self, host, port, password, logger=LOGS, *args, **kwargs):
        if host and ":" in host:
            spli_ = host.split(":")
            host = spli_[0]
            port = int(spli_[-1])
            if host.startswith("http"):
                logger.error("Your REDIS_URI should not start with http !")
                import sys
                sys.exit()
        elif not host or not port:
            logger.error("Port Number not found")
            import sys
            sys.exit()
        kwargs["host"] = host
        kwargs["password"] = password
        kwargs["port"] = port

        self.db = Redis(**kwargs)
        self.set = self.db.set
        self.get = self.db.get
        self.keys = self.db.keys
        self.delete = self.db.delete
        super().__init__()

    @property
    def name(self):
        return "REDIS"

    @property
    def usage(self):
        return sum(self.db.memory_usage(x) for x in self.keys())


def pyDatabase():
    _er = False
    try:
        if Redis:
            return RedisDB(
                host=Var.REDIS_URI or Var.REDISHOST,
                password=Var.REDIS_PASSWORD,
                port=Var.REDISPORT,
                decode_responses=True,
                socket_timeout=5,
                retry_on_timeout=True,
            )
    except BaseException as err:
        LOGS.exception(err)
        _er = True
    if not _er:
        LOGS.critical(
            "No DB requirement fullfilled!\nPlease install redis."
        )
        return
    exit()

