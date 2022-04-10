def join_urls(*args) -> str:
    """Join URL parts (they may be absolute or relative)

    Returns:
        a url of form /some/endpoint/object_2/
    """
    url = ""
    for entry in args:
        if not entry:
            continue
        url += entry.strip("/") + "/"
    url = url.rstrip("/") + "/"
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return "/" + url
