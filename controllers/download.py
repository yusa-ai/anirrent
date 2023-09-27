import threading

from psycopg2.extensions import connection, cursor
from pydantic import UUID4

from models.download import DownloadIn, DownloadUUID
from utils.torrent import Torrent


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
        response = cur.fetchone()

        if download.season and download.episode:
            file_name = f"{download.entry_name} - S{download.season:02d}E{download.episode:02d}.mkv"
        else:
            file_name = f"{download.entry_name}.mkv"

        # Initiate torrent download
        torrent = Torrent(
            download.magnet_url,
            file_name,
            "./output/",
            response["download_uuid"],
            conn,
            cur,
        )
        threading.Thread(target=torrent.download).start()

        return response
