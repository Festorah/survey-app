from sanic import Sanic

from config.settings import settings
from src.exceptions import handle_exception

from .logger import setup_logging
from .routes import bp

# Initialize the Sanic app
app = Sanic("SurveyApp")

# Set up centralized logging
logger = setup_logging()

# Static and template setup
app.static("/static", "./static")
app.config.TEMPLATES_FOLDER = "./templates"

# Register blueprints
app.blueprint(bp)

# Register error handler middleware
app.error_handler.add(Exception, handle_exception)

if __name__ == "__main__":
    app.run(
        host=settings.HOST, port=settings.PORT, auto_reload=True, debug=settings.DEBUG
    )
