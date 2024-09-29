from api.v1.app import app
from os import getenv

host = getenv("API_HOST", "0.0.0.0")
port = getenv("API_PORT", "5000")
app.run(host=host, port=port)