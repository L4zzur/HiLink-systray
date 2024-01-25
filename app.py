import sys
import time
from infi.systray import SysTrayIcon
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from datetime import timedelta


def get_human_readable_size(size: int, decimal_places: int = 2):
    for unit in ["bps", "Kbps", "Mbps", "Gbps", "Tbps"]:
        if size < 1024:
            if unit == "bps":
                decimal_places = 0
            break
        size /= 1024
    return f"{round(size, decimal_places)} {unit}"


class TrafficInfo:
    def __init__(self, ip: str) -> None:
        self.client = Client(Connection(ip))

    def get_traffic_info(self) -> dict:
        return self.client.monitoring.traffic_statistics()

    def get_current_connect_time(self) -> timedelta:
        return timedelta(seconds=int(self.get_traffic_info()["CurrentConnectTime"]))

    def get_upload_speed_bps(self) -> int:
        return int(self.get_traffic_info()["CurrentUploadRate"]) * 8

    def get_download_speed_bps(self) -> int:
        return int(self.get_traffic_info()["CurrentDownloadRate"]) * 8

    def get_upload_speed(self) -> str:
        return get_human_readable_size(self.get_upload_speed_bps())

    def get_download_speed(self) -> str:
        return get_human_readable_size(self.get_download_speed_bps())

    def get_current_upload_bps(self) -> int:
        return int(self.get_traffic_info()["CurrentUpload"])

    def get_current_download_bps(self) -> int:
        return int(self.get_traffic_info()["CurrentDownload"])

    def get_current_upload(self) -> str:
        return get_human_readable_size(self.get_current_upload_bps())

    def get_current_download(self) -> str:
        return get_human_readable_size(self.get_current_download_bps())


client = TrafficInfo("http://192.168.8.1/")


systray = SysTrayIcon("icon.ico", "HiLink LTE Monitor")
systray.start()


while True:
    try:
        connect_time = client.get_current_connect_time()
        download_speed = client.get_download_speed()
        upload_speed = client.get_upload_speed()
        current_download = client.get_current_download()
        current_upload = client.get_current_upload()

        info_string = f"Time: {connect_time} \nDownload Speed: {download_speed} \nUpload Speed: {upload_speed} \n\nCurrent Download: {current_download} \nCurrent Upload: {current_upload}"

        if not systray.is_running():
            break
        systray.update(hover_text=info_string)
        time.sleep(2)
    except KeyboardInterrupt:
        systray.shutdown()
        exit()
