import sqlite3

from fbsrankings.infrastructure.sqlite.storage import SeasonSectionTable, SeasonTable, TeamTable, SubdivisionTable, AffiliationTable, GameStatusTable, GameTable


class Storage (object):
    def __init__(self, database: str) -> None:
        self.database = database
        
        connection = sqlite3.connect(database)
        try:
            connection.isolation_level = None
            connection.execute('PRAGMA foreign_keys = ON')
        
            cursor = connection.cursor()
            cursor.execute("begin")
            try:
                SeasonSectionTable().create(cursor)
                SubdivisionTable().create(cursor)
                GameStatusTable().create(cursor)
        
                SeasonTable().create(cursor)
                TeamTable().create(cursor)
                AffiliationTable().create(cursor)
                GameTable().create(cursor)
        
                cursor.execute("commit")
            except:
                cursor.execute("rollback")
                raise
            finally:
                cursor.close()
        finally:
            connection.close()
