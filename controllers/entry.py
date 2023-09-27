from psycopg2.extensions import connection, cursor
from pydantic import UUID4

from models.entry import EntryIn, EntryOut, EntryType, EntryUUID


class EntryController:
    @staticmethod
    def get_entries(cur: cursor, entry_type: EntryType | None = None) -> list[EntryOut]:
        if entry_type:
            cur.execute("SELECT * FROM entries WHERE entry_type = %s;", (entry_type,))
        else:
            cur.execute("SELECT * FROM entries;")
        response = cur.fetchall()
        return response

    @staticmethod
    def post_entry(conn: connection, cur: cursor, entry: EntryIn) -> EntryUUID:
        cur.execute(
            "INSERT INTO entries (entry_name, entry_type) VALUES (%s, %s) RETURNING entry_uuid;",
            (entry.entry_name, entry.entry_type),
        )
        conn.commit()
        response = cur.fetchone()
        return response
