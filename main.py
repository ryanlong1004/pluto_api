from dataclasses import dataclass
import datetime
import json
from typing import Any, Dict, List
import requests

urls = {
    "main_catalog": "https://service-media-catalog.clusters.pluto.tv/v1/main-categories?includeImages=svg",
    "catgories": "https://service-vod.clusters.pluto.tv/v4/vod/categories?includeItems=false&includeCategoryFields=iconSvg&offset=1000&page=1&sort=number%3Aasc",
    "channels": "https://service-channels.clusters.pluto.tv/v2/guide/channels?channelIds=&offset=0&limit=1000&sort=number%3Aasc",
}


@dataclass
class NowPlayingItem:
    title: str
    start: str
    description: str
    poster_url: str


class Pluto:
    def __init__(self):
        self._bearer_token = None
        self.start = "2022-12-18T21:30:00.000Z"
        self.channelIds = "569546031a619b8f07ce6e25,5c6dc88fcd232425a6e0f06e,5a4d3a00ad95e4718ae8d8db,5f4d863b98b41000076cd061"
        self.duration = 240
        self._live = None

    @property
    def live(self) -> Dict[Any, Any]:
        if self._live is None:
            self._live = self._fetch_update()
        return self._live

    @property
    def start_time(self):
        return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:00.000Z")

    @property
    def bearer_token(self):
        if self._bearer_token == None:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://pluto.tv/",
                "Origin": "https://pluto.tv",
                "DNT": "1",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
            }

            response = requests.get(
                "https://boot.pluto.tv/v4/start?appName=web&appVersion=6.9.0-43d41e8a49dba2d9f77dd4d6b0ab9aba87e68c24&deviceVersion=107.0.0&deviceModel=web&deviceMake=firefox&deviceType=web&clientID=1be65127-0e29-45b4-bf17-76cf7ab47d96&clientModelNumber=1.0.0&channelSlug=pluto-tv-horror&serverSideAds=true&constraints=&drmCapabilities=widevine%3AL3&clientTime=2022-12-18T22%3A42%3A13.851Z",
                headers=headers,
            )
            self._bearer_token = response.json()["sessionToken"]
        return self._bearer_token

    def now_playing(self) -> List[NowPlayingItem]:
        timelines = [x["timelines"] for x in self.live["data"]]
        result = []
        for x in timelines:
            for y in x:
                print(y)
                result.append(
                    NowPlayingItem(
                        f"{y['title']}",
                        f"{y['start']}",
                        f"{y['episode']['description']}",
                        f"{y['episode']['poster']['path']}",
                    )
                )
        return result

    def _fetch_update(self):
        url2 = f"https://service-channels.clusters.pluto.tv/v2/guide/timelines?start={self.start_time}&channelIds={self.channelIds}&duration=240"

        headers = {
            "Host": "service-channels.clusters.pluto.tv",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Authorization": f"Bearer {self.bearer_token}",
            "Referer": "https://pluto.tv/",
            "Origin": "https://pluto.tv",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers",
        }

        response = requests.get(url2, headers=headers)
        return json.loads(response.content.decode())


if __name__ == "__main__":
    pluto = Pluto()
    for x in pluto.now_playing():
        # print(x.poster_url)
        print(x.title)
