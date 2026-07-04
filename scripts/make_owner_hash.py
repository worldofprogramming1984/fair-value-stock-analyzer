"""Generate the OWNER_PASSPHRASE_HASH for the app's owner mode.

Usage:
    python scripts/make_owner_hash.py "my secret passphrase"
    python scripts/make_owner_hash.py            # prompts securely

Put the printed value in Streamlit Cloud → app → Settings → Secrets as:
    OWNER_PASSPHRASE_HASH = "…"
(or export it as an env var locally). Only the hash is stored — never the passphrase.
"""
import getpass
import hashlib
import sys


def main() -> None:
    phrase = sys.argv[1] if len(sys.argv) > 1 else getpass.getpass("Owner passphrase: ")
    phrase = phrase.strip()
    if not phrase:
        print("Empty passphrase — aborting.")
        raise SystemExit(1)
    digest = hashlib.sha256(phrase.encode("utf-8")).hexdigest()
    print("\nAdd this to Streamlit secrets (or export as env var):")
    print(f'OWNER_PASSPHRASE_HASH = "{digest}"')


if __name__ == "__main__":
    main()
