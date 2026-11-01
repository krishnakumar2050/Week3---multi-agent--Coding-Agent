"""Credential tests never access the real Keychain or provider."""

from types import SimpleNamespace

import pytest

from coding_review import credentials
from coding_review.exceptions import ConfigurationError


@pytest.fixture(autouse=True)
def isolated_keychain(monkeypatch):
    monkeypatch.delenv("FIREWORKS_API_KEY", raising=False)
    monkeypatch.setattr(credentials.sys, "platform", "darwin")
    monkeypatch.setattr(credentials, "_keychain", lambda: SimpleNamespace(get_password=lambda *a: None))


def test_environment_precedes_keychain(monkeypatch):
    monkeypatch.setenv("FIREWORKS_API_KEY", " env-secret ")
    monkeypatch.setattr(credentials, "_keychain", lambda: pytest.fail("Keychain accessed"))
    assert credentials.load_fireworks_key() == "env-secret"


def test_native_keychain_lookup(monkeypatch):
    def read(service, account):
        assert (service, account) == (credentials.SERVICE, credentials.ACCOUNT)
        return "saved-secret"
    monkeypatch.setattr(credentials, "_keychain", lambda: SimpleNamespace(get_password=read))
    assert credentials.load_fireworks_key() == "saved-secret"


def test_keychain_errors_do_not_leak_secret(monkeypatch):
    def fail(*args):
        raise RuntimeError("sensitive-secret")
    monkeypatch.setattr(credentials, "_keychain", lambda: SimpleNamespace(get_password=fail))
    with pytest.raises(ConfigurationError) as error:
        credentials.load_fireworks_key()
    assert "sensitive-secret" not in str(error.value)


def test_missing_key_is_actionable():
    with pytest.raises(ConfigurationError, match="FIREWORKS_API_KEY"):
        credentials.load_fireworks_key()


def test_status_hides_value(monkeypatch, capsys):
    monkeypatch.setenv("FIREWORKS_API_KEY", "secret-value")
    credentials.main(["status"])
    output = capsys.readouterr().out
    assert "configured" in output
    assert "secret-value" not in output


def test_setup_stores_hidden_input(monkeypatch, capsys):
    stored = []
    monkeypatch.setattr(credentials, "_keychain", lambda: SimpleNamespace(
        set_password=lambda *args: stored.append(args)))
    monkeypatch.setattr(credentials.sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(credentials.getpass, "getpass", lambda prompt: "secret-value")
    credentials.main(["set"])
    assert stored == [(credentials.SERVICE, credentials.ACCOUNT, "secret-value")]
    assert "secret-value" not in capsys.readouterr().out


def test_setup_rejects_noninteractive_input(monkeypatch):
    monkeypatch.setattr(credentials.sys.stdin, "isatty", lambda: False)
    monkeypatch.setattr(credentials.getpass, "getpass", lambda *a: pytest.fail("prompted"))
    with pytest.raises(SystemExit):
        credentials.main(["set"])
