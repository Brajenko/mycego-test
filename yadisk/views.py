from django.shortcuts import render

from django.http import HttpRequest
from .utils.yadisk_api import get_public_folder_items, YandexApiError


def explorer(request: HttpRequest):
    public_key = request.GET.get("public_key", "")
    sort = request.GET.get("sort", "created")
    reverse = request.GET.get("reverse", "false") == "true"
    path = request.GET.get("path", "")

    context = {"path": path, "public_key": public_key, "sort": sort, "reverse": reverse}
    try:
        items = get_public_folder_items(
            public_key,
            path=path,
            sort=sort,
            reverse=reverse,
        )
    except YandexApiError as e:
        context.update({"error": str(e)})
    else:
        context.update({"items": items})
    return render(request, "yadisk/explorer.html", context)
