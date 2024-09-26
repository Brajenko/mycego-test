import requests

import datetime as dt


class YandexApiError(Exception):
    pass


BASE_URL = "https://cloud-api.yandex.net/v1/disk"

FIELDS = [
    "public_key",
    "public_url",
]

ITEM_FIELDS = [
    "created",
    "modified",
    "name",
    "file",
    "preview",
    "public_key",
    "type",
    "path",
]

FIELDS_PARAM = ",".join(FIELDS + ["_embedded.items." + f for f in ITEM_FIELDS])


def _default_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(
        {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "OAuth ",
        }
    )
    return s


def get_public_folder_items(
    public_url: str, path: str, sort: str, reverse: bool
) -> list[dict]:
    s = _default_session()
    resp = s.get(
        BASE_URL + "/public/resources/",
        params={
            "public_key": public_url,
            "path": path,
            "sort": ("-" if reverse else "") + sort,
            "fields": FIELDS_PARAM,
        },
    )
    data = resp.json()
    err = data.get('error', None)
    if err is not None:
        raise YandexApiError(data['message'])
    items = data["_embedded"]["items"]
    for item in items:
        item["created"] = dt.datetime.fromisoformat(item["created"])
        item["modified"] = dt.datetime.fromisoformat(item["modified"])

    return items
