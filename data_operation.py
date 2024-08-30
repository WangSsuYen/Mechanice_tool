from config import DATABASE_URI
from sqlalchemy import Connection

class database_operation:
    def __init__(self) -> None:
        self.cour = Connection(DATABASE_URI)

    def Insert(self):
        pass

    def Delete(self):
        pass

    def Motify(self):
        pass
