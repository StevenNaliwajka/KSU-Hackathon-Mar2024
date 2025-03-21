from API.Codebase.DB.database import Database


def connect_to_db():
    db = Database()
    return db