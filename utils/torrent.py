import os
import time

import libtorrent as lt
from psycopg2.extensions import connection, cursor


class Torrent:
    def __init__(
        self,
        magnet_url: str,
        file_name: str,
        save_path: str,
        download_uuid: str,
        conn: connection,
        cur: cursor,
    ) -> None:
        self._magnet_url = magnet_url
        self._save_path = save_path
        self._file_name = file_name
        self._download_uuid = download_uuid
        self._conn = conn
        self._cur = cur

        # Create the directory if it doesn't exist
        os.makedirs(self._save_path, exist_ok=True)

        self._session = lt.session({"listen_interfaces": "0.0.0.0:6881"})
        self._add_torrent_params = lt.parse_magnet_uri(self._magnet_url)
        self._add_torrent_params.renamed_files = {0: self._file_name}
        self._add_torrent_params.save_path = self._save_path

    def download(self) -> str:
        self._handle = self._session.add_torrent(self._add_torrent_params)

        while not self._status.is_seeding:
            self._status = self._handle.status()

            # Update progress in the database
            progress_percentage = f"{(self._status.progress * 100):.2f}"

            query = "UPDATE downloads SET progress = %s WHERE download_uuid = %s;"
            params = (progress_percentage, self._download_uuid)
            self._cur.execute(query, params)
            self._conn.commit()

            time.sleep(1)

        return f"{self._status.save_path}{self._file_name}"
