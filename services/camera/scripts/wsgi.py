import logging
from app import app

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers

if __name__ == "__main__":
    app.run()

