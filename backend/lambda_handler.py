# lambda_handler.py
import serverless_wsgi
from app import app  # Imports your main Flask app

def handler(event, context):
    """
    This function is called by Lambda.
    It passes the request to your Flask app.
    """
    return serverless_wsgi.handle_request(app, event, context)
