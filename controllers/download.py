from psycopg2.extensions import connection, cursor
from pydantic import UUID4

from models.download import DownloadIn, DownloadUUID


class DownloadController:
    @staticmethod
    def post_download(
        conn: connection, cur: cursor, download: DownloadIn
    ) -> DownloadUUID:
        query = "INSERT INTO downloads (magnet_url, entry_name, season, episode) VALUES (%s, %s, %s, %s) RETURNING download_uuid;"
        params = (
            download.magnet_url,
            download.entry_name,
            download.season,
            download.episode,
        )
        cur.execute(query, params)
        conn.commit()
        download_uuid = cur.fetchone()

        # TODO Initiate torrent download

        return download_uuid
