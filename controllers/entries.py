from psycopg2.extensions import connection, cursor
from pydantic import UUID4

from models.entry import EntryIn, EntryOut, EntryType


class EntriesController:
    @staticmethod
    def get_entries(cur: cursor, entry_type: str | None = None) -> list[EntryOut]:
        if entry_type:
            cur.execute("SELECT * FROM entries WHERE entry_type = %s;", (entry_type,))
        else:
            cur.execute("SELECT * FROM entries;")
        entries = cur.fetchall()
        return entries

    @staticmethod
    def post_entry(conn: connection, cur: cursor, entry: EntryIn) -> EntryOut:
        cur.execute(
            "INSERT INTO entries (entry_name, entry_type) VALUES (%s, %s) RETURNING entry_uuid;",
            (entry.entry_name, entry.entry_type),
        )
        conn.commit()
        entry_uuid = cur.fetchone()
        return entry_uuid
