import importlib
import sys
import types


class DummyResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def json(self):
        return self._payload


class DummyRequestException(Exception):
    pass


def _build_dummy_requests():
    return types.SimpleNamespace(
        get=lambda *args, **kwargs: DummyResponse(500),
        codes=types.SimpleNamespace(ok=200),
        exceptions=types.SimpleNamespace(RequestException=DummyRequestException),
    )


def _get_api_class(monkeypatch):
    monkeypatch.setitem(sys.modules, "requests", _build_dummy_requests())
    api_module = importlib.import_module("custom_components.em6.api")
    importlib.reload(api_module)
    return api_module.em6Api


def test_get_prices_handles_http_error(monkeypatch):
    em6Api = _get_api_class(monkeypatch)

    def fake_get(*args, **kwargs):
        return DummyResponse(500)

    import requests
    monkeypatch.setattr(requests, "get", fake_get)

    api = em6Api("Somewhere")
    assert api.get_prices() is None


def test_get_prices_handles_request_exception(monkeypatch):
    em6Api = _get_api_class(monkeypatch)

    import requests

    def raise_error(*args, **kwargs):
        raise requests.exceptions.RequestException("boom")

    monkeypatch.setattr(requests, "get", raise_error)

    api = em6Api("Somewhere")
    assert api.get_prices() is None
