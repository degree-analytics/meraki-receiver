from typing import Dict, Any
import enum
import simplejson as json
from datetime import *
import requests

import unicodedata


class RequestStatusException(Exception):
    status_code: int

    def __init__(self, status_code, text):
        super(RequestStatusException, self).__init__("{}: {}".format(status_code, text))
        self.status_code = status_code


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def jsonify(dictionary, **kwargs):
    def default(o):
        if hasattr(o, "to_dict"):
            return o.to_dict()
        elif hasattr(o, "serialize"):
            return o.serialize()
        elif isinstance(o, datetime):
            return int((o - datetime.utcfromtimestamp(0)).total_seconds())
        elif isinstance(o, set):
            return list(o)
        elif isinstance(o, (enum.Enum, enum.IntEnum)):
            return o.value
        elif isinstance(o, str):
            return remove_accents(o)
        return remove_accents(str(o))

    out = json.dumps(dictionary, default=default, use_decimal=True, ensure_ascii=False, **kwargs).encode('utf8')
    return out


class MerakiAPI(object):
    base_url = 'https://api.meraki.com/api/v0/'

    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            'x-cisco-meraki-api-key': self.api_key
        }

    @classmethod
    def _response(cls, out):
        if out.status_code == 200:
            return out.json()

        raise RequestStatusException(out.status_code, out.text)

    def _build_url(self, url: str) -> str:
        return self.base_url + url

    def get(self, url: str, params: dict = {}):
        url = self._build_url(url=url)
        return self._response(requests.get(url=url, headers=self.headers, params=params))

    def post(self, url: str, body: Dict[str, Any], params: Dict[str, Any] = None):
        url = self._build_url(url=url)
        return self._response(requests.post(url=url, data=jsonify(body), params=params, headers=self.headers))

    def put(self, url: str, body: Dict[str, Any], params: Dict[str, Any] = None):
        url = self._build_url(url=url)
        return self._response(requests.put(url=url, data=jsonify(body), params=params, headers=self.headers))

    def delete(self, url: str, params: Dict[str, Any] or None = None):
        url = self._build_url(url=url)
        return self._response(requests.delete(url=url, params=params, headers=self.headers))
