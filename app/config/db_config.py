from flask_sqlalchemy import SQLAlchemy

class DatabaseManager:
    _instance = None
    _db = None
    
    def __new__(cls, app=None):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)

        cls._db = SQLAlchemy(app) if app else SQLAlchemy()
        return cls._instance
    
    def init_app(self, app):
        if self._db:
            self._db.init_app(app)
    
    @property    
    def db(self):
        return self._db

db_manager = DatabaseManager()
db = db_manager.db