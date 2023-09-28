import threading

from psycopg2.extensions import connection, cursor
from pydantic import UUID4

from models.download import DownloadIn, DownloadOut, DownloadUUID
from utils.media_server import MediaServer
from utils.torrent import Torrent


class DownloadController:
    @staticmethod
    def get_download(cur: cursor, download_uuid: UUID4) -> DownloadOut:
        query = "SELECT * FROM downloads WHERE download_uuid = %s;"
        params = (download_uuid,)
        cur.execute(query, params)
        response = cur.fetchone()
        return response

    @staticmethod
    def _download_and_upload(download, response, conn, cur):
        tv_show = download.season and download.episode

        if tv_show:
            file_name = f"{download.entry_name} - S{download.season:02d}E{download.episode:02d}.mkv"
        else:
            file_name = f"{download.entry_name}.mkv"

        torrent = Torrent(
            download.magnet_url,
            file_name,
            "./output/",
            response["download_uuid"],
            conn,
            cur,
        )

        destination_folder = "anime" if tv_show else "anime_movies"
        remote_path = f"Disque 1/{destination_folder}/{download.entry_name}"

        file_path = torrent.download()
        MediaServer.upload(file_path=file_path, remote_path=remote_path)

        query = "UPDATE uploads SET status = 'COMPLETE' WHERE download_uuid = %s;"
        params = (response["download_uuid"],)
        cur.execute(query, params)
        conn.commit()

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

        threading.Thread(
            target=DownloadController._download_and_upload,
            args=(download, response, conn, cur),
        ).start()

        return response
