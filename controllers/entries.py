from psycopg2.extensions import cursor

from models.entry import Entry


class EntriesController:
    @staticmethod
    def get_entries(cur: cursor, entry_type: str | None = None) -> list[Entry]:
        if entry_type:
            cur.execute("SELECT * FROM entries WHERE entry_type = %s;", (entry_type,))
        else:
            cur.execute("SELECT * FROM entries;")
        entries = cur.fetchall()
        return entries
