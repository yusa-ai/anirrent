import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from controllers.entries import EntriesController
from models.entry import EntryType, Entry

app = FastAPI(title="Anirrent", version="1.0.0")

conn = psycopg2.connect(
    dbname="anirrent",
    user="postgres",
    password="postgres",
    host="192.168.1.5",
    cursor_factory=RealDictCursor,
)
cur = conn.cursor()


@app.get("/v1/entries")
def get_entries(entry_type: EntryType | None = None) -> list[Entry]:
    entries = EntriesController.get_entries(cur, entry_type)
    return entries
