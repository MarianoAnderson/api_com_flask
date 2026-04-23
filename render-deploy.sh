set -e

poetry run python --app src.app db upgrade
poetry run gunicorn --bind