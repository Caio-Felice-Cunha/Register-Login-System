"""Pytest configuration.

Point the app at a throwaway SQLite database before any application module is
imported, so tests never touch the real userDB.db file in the repo.
"""

import os
import tempfile

# Must be set before models.py is imported (it reads DATABASE_URL at import time).
_TEST_DB = os.path.join(tempfile.gettempdir(), "rls_test.db")
if os.path.exists(_TEST_DB):
    os.remove(_TEST_DB)
os.environ["DATABASE_URL"] = f"sqlite:///{_TEST_DB}"
