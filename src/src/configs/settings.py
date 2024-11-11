from .base import *

ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")

# Redis settings
REDIS_EXPIRATION_TIME = os.environ.get("REDIS_EXPIRATION_TIME", 3600)
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)

# Token settings
ACCESS_TOKEN_EXPIRE_TIME = os.environ.get("ACCESS_TOKEN_EXPIRE_TIME", 3600)
REFRESH_ACCESS_TOKEN_EXPIRE_TIME = os.environ.get(
    "REFRESH_ACCESS_TOKEN_EXPIRE_TIME", 3600 * 24
)
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET", "access-token-secret")
REFRESH_TOKEN_SECRET = os.environ.get("REFRESH_TOKEN_SECRET", "refresh-token-secret")

# Swagger Setting
SPECTACULAR_SETTINGS = {
    "TITLE": "App API",
    "DESCRIPTION": "App API for Data Mining App",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "SCHEMA_PATH_PREFIX": "/api/v1",
    "SCHEMA_PATH_PREFIX_TRIM": False,
}
JWT_SECRET_KEY = os.environ.get("JWT_SECRET", "jwt-secret")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_TIME = os.environ.get("JWT_EXPIRE_TIME", 3600)

# Database settings
# AUTH_USER_MODEL = "home.User"