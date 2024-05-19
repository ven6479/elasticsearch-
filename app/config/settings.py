import os

from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

if load_dotenv(BASE_DIR / '.env') is False:
    raise AssertionError(f"File .env not found, search directory: {BASE_DIR / '.env'}")

DB_FILE = os.getenv('DATABASE_USER', 'testdb.sqlite3')

INITIAL_DATA_DIR = BASE_DIR / 'initial_data.txt'

ELASTIC_CREDS = {
    "hosts": os.getenv('ELASTIC_HOST', 'https://localhost:9200'),
    "basic_auth": (
        os.getenv('ELASTIC_TYPE_AUTH', 'elastic'),
        os.getenv('ELASTIC_PASSWORD', 'password')
    ),
    "ca_certs": os.getenv('ELASTIC_CERTS', 'path/to/certs')
}
