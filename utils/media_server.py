import os
from ftplib import FTP


class MediaServer:
    @staticmethod
    def upload(file_path: str, remote_path: str) -> bool:
        host = os.environ.get("FTP_HOST")
        user = os.environ.get("FTP_USER")
        passwd = os.environ.get("FTP_PWD")

        if not host or not user or not passwd:
            raise KeyError("Missing environment variable")

        with FTP(host=host, user=user, passwd=passwd) as ftp, open(
            file_path, "rb"
        ) as file:
            ftp.cwd(remote_path)
            ftp.storbinary(f"STOR {os.path.basename(file_path)}", file)

        os.remove(file_path)
        return True
