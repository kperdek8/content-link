class DefaultConfig:
    """
    Default configuration, in case .env variables are missing.
    """
    def __init__(self):
        # App
        self.APP_NAME = "Content-link"
        # MySQL
        self.MYSQL_HOST = '0.0.0.0'
        self.MYSQL_PORT = '3306'
        self.MYSQL_USER = 'user'
        self.MYSQL_PASSWORD = 'password'
        self.MYSQL_DB = 'wordpress'
