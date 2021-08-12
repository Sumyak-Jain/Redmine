import requests

_get_json = lambda _url, _hdr : requests.get(_url, headers = _hdr)

def get_json(_url, _hdr):
    try:
        _json = _get_json(_url, _hdr)
        _json.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise Exception
    except requests.exceptions.RequestException as err:
        raise Exception

    return _json.json()

def post_data(_url, _data,_hdr):
    try:
        _ret = requests.post(url = _url, data = _data, headers = _hdr)
        print(_ret)
        return _ret
    except requests.exceptions.RequestException as err:
        raise Exception
    except requests.exceptions.HTTPError as err:
        raise Exception
