import os


class ConfigurationError(KeyError):
    pass


class DBConfig:
    """ env vars for database configuration. """

    def __init__(self):
        try:
            self.POSTGRES_USER = os.environ["POSTGRES_USER"]
            self.POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
            self.POSTGRES_DB = os.environ["POSTGRES_DB"]
            self.POSTGRES_HOST = os.environ["POSTGRES_HOST"]
            self.POSTGRES_PORT = os.environ["POSTGRES_PORT"]
            self.POSTGRES_SCHEMA = os.environ["POSTGRES_SCHEMA"]
        except KeyError as ex:
            raise ConfigurationError(f"Unable to get configuration value: {ex.args[0]}.")
    
    @property
    def sa_connection_string(self):
        """ Connection string for creating sqlalchemy engine object. """
        
        return 'postgresql+asyncpg://{}:{}@{}:{}/{}'.format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB
        )


if __name__ == "__main__":
    c = DBConfig()
    print(c.connection_string)
