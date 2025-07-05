# auth0/auth_protector.py
from dotenv import load_dotenv
from os import getenv

from authlib.integrations.flask_oauth2 import ResourceProtector
from auth0.token_validator import Auth0JWTBearerTokenValidator

load_dotenv()


def load_require_auth():
    resource_protector = ResourceProtector()

    domain = getenv('AUTH0_DOMAIN')
    audience = getenv('AUTH0_AUDIENCE')

    validator = Auth0JWTBearerTokenValidator(
        f"{domain}",
        f"{audience}"
    )

    resource_protector.register_token_validator(validator)
    return resource_protector


require_auth = load_require_auth()