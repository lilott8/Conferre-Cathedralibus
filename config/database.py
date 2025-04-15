

class Database(object):

    def __init__(self, db):
        self.user = db.get('user')
        self.password = db.get('password')
        self.port = db.get('port')
        self.host = db.get('host')
        self.db_name = db.get("db_name")

    def get_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

    def get_db_url_sync(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

    def __repr__(self):
        return f"User: {self.user}, Port: {self.port}, Host: {self.host}, DB Name: {self.db_name}, Password: <<omitted>>"
