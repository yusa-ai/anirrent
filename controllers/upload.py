from psycopg2.extensions import cursor
from pydantic import UUID4

from models.upload import UploadOut


class UploadController:
    @staticmethod
    def get_upload(cur: cursor, download_uuid: UUID4) -> UploadOut:
        query = "SELECT status FROM uploads WHERE download_uuid = %s;"
        params = (download_uuid,)
        cur.execute(query, params)
        response = cur.fetchone()
        return response
