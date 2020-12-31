"""
    Initial Flask application routine
"""

from flask import Flask, render_template


app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500


# Import modules using blueprint handlers
from app.index_page.controllers import index as index_module

# Register blueprints
app.register_blueprint(index_module)


