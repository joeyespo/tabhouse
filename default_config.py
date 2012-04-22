"""\
Default Config

Do NOT change the values here.
Override them in the instance/application_config.py file instead.
"""


# Development settings
DEBUG = None
HOST = 'localhost'
PORT = 5000

# Logging defaults
LOGGING = {
    'version': 1,
    'handlers': { 'console': { 'level': 'DEBUG', 'class': 'logging.StreamHandler', } },
    'loggers': { None: { 'handlers': ['console'], 'level': 'DEBUG', } }
}

# Security settings
SECRET_KEY = None

# Logging settings
ERROR_EMAIL_INFO = None     # Format: ((HOST, PORT), FROM_ADDRESS, (TO_ADDRESS, ...), SUBJECT, (EMAIL_USER, EMAIL_PASS))

# User feedback settings
ANALYTICS_SCRIPT = None
FEEDBACK_BLOCK = None
