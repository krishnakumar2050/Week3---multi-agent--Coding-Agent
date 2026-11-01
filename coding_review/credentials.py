"""Load Fireworks secrets without writing them to the repository."""

import argparse
import getpass
import os
import sys
import warnings

from coding_review.exceptions import ConfigurationError

SERVICE = "coding-review.fireworks"
ACCOUNT = "FIREWORKS_API_KEY"


def _keychain():
    if sys.platform != "darwin":
        raise ConfigurationError("Native Keychain requires macOS; use FIREWORKS_API_KEY in CI.")
    try:
        # Pin the OS backend to prevent plaintext backend fallback.
        from keyring.backends.macOS import Keyring

        return Keyring()
    except ImportError:
        raise ConfigurationError(
            'Install credential support: python -m pip install -e ".[credentials]"'
        ) from None


def load_fireworks_key():
    value = os.getenv(ACCOUNT, "").strip()
    if value:
        return value
    if sys.platform == "darwin":
        try:
            value = _keychain().get_password(SERVICE, ACCOUNT)
        except ConfigurationError:
            value = None
        except Exception:
            raise ConfigurationError("Unable to read Fireworks key; unlock macOS Keychain and retry.") from None
        if value and value.strip():
            return value.strip()
    raise ConfigurationError(
        "Configure FIREWORKS_API_KEY with python -m coding_review.credentials set "
        "or inject it using your CI secret manager."
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Configure Fireworks using macOS Keychain.")
    parser.add_argument("action", choices=["set", "status"])
    args = parser.parse_args(argv)
    try:
        if args.action == "status":
            load_fireworks_key()
            print("Fireworks credential configured (value hidden; API access not validated).")
            return
        backend = _keychain()
        if not sys.stdin.isatty():
            raise ConfigurationError("Run setup in an interactive terminal with hidden input.")
        with warnings.catch_warnings():
            warnings.simplefilter("error", getpass.GetPassWarning)
            try:
                value = getpass.getpass("Fireworks API key (hidden): ").strip()
            except getpass.GetPassWarning:
                raise ConfigurationError("Secure hidden input is unavailable.") from None
        if not value:
            raise ConfigurationError("API key must not be empty.")
        try:
            backend.set_password(SERVICE, ACCOUNT, value)
        except Exception:
            raise ConfigurationError("Could not save credential in macOS Keychain.") from None
        finally:
            value = None
        print("Fireworks key saved in macOS Keychain; no key written to the project.")
    except ConfigurationError as exc:
        parser.error(str(exc))
    except (EOFError, KeyboardInterrupt):
        parser.exit(1, "Credential setup cancelled.\n")


if __name__ == "__main__":
    main()
