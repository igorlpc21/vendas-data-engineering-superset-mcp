"""Configuração exclusiva do laboratório Docker isolado, sem segredos no código."""
import os
from urllib.parse import quote_plus

SECRET_KEY = os.environ["SUPERSET_SECRET_KEY"]
db_user = quote_plus(os.environ["POSTGRES_USER"])
db_password = quote_plus(os.environ["POSTGRES_PASSWORD"])
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{db_user}:{db_password}@postgres:5432/superset"
)
MCP_AUTH_ENABLED = False
MCP_DEV_USERNAME = os.environ.get("SUPERSET_ADMIN_USER", "admin")
SUPERSET_WEBSERVER_ADDRESS = (
    f"http://localhost:{os.environ.get('DEMO_SUPERSET_PORT', '18888')}"
)
WTF_CSRF_ENABLED = True
TALISMAN_ENABLED = False  # HTTP local; não é configuração de produção.
