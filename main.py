import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor

from controllers.download import DownloadController
from controllers.entry import EntryController
from controllers.upload import UploadController
from models.download import DownloadIn, DownloadOut, DownloadUUID
from models.entry import EntryIn, EntryOut, EntryType, EntryUUID
from models.upload import UploadOut

app = FastAPI(title="Anirrent", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

conn = psycopg2.connect(
    dbname="anirrent",
    user="postgres",
    password="postgres",
    host="192.168.1.5",
    cursor_factory=RealDictCursor,
)
cur = conn.cursor()


@app.get("/v1/download/{download_uuid}")
def get_download(download_uuid: str) -> DownloadOut:
    download = DownloadController.get_download(cur, download_uuid)
    return download


@app.post("/v1/download")
def post_download(download: DownloadIn) -> DownloadUUID:
    download_uuid = DownloadController.post_download(conn, cur, download)
    return download_uuid


@app.get("/v1/upload/{download_uuid}")
def get_upload(download_uuid: str) -> UploadOut:
    upload = UploadController.get_upload(cur, download_uuid)
    return upload


@app.get("/v1/entries")
def get_entries(entry_type: EntryType | None = None) -> list[EntryOut]:
    entries = EntryController.get_entries(cur, entry_type)
    return entries


@app.post("/v1/entries")
def post_entry(entry: EntryIn) -> EntryUUID:
    entry_uuid = EntryController.post_entry(conn, cur, entry)
    return entry_uuid
