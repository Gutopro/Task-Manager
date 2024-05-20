import jwt
import datetime
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import UserModel
import logging

logger = logging.getLogger(__name__)

# Ensure the secret and algorithm are defined in settings
secret = getattr(settings, 'SECRET_KEY', 'your_secret_key')  # Preferably use settings.SECRET_KEY
algorithm = 'HS256'

def generate_token(user):
    """Generate a token for a particular user after login"""
    try:
        payload = {
            "user_id": user.id,
            "user_email": user.email,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7),
            "iss": "gutopro",
            "iat": datetime.datetime.now(datetime.timezone.utc),
        }
        token = jwt.encode(payload, secret, algorithm)
        logger.debug(f"Generated token for user {user.id}: {token}")
        return token
    except Exception as e:
        logger.error(f"Token generation error: {e}")
        return None

def get_user_from_request(request):
    """Retrieves a user from a token"""
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.split(' ', 1)[1]
        try:
            payload = jwt.decode(token, secret, algorithms=[algorithm], issuer="gutopro")
            user_id = payload.get("user_id")
            logger.debug(f"Extracted user_id from token: {user_id}")
            
            if user_id:
                try:
                    user = UserModel.objects.get(pk=user_id)
                    logger.debug(f"Found user {user_id} in database")
                    return user
                except UserModel.DoesNotExist:
                    logger.error(f"User with id {user_id} not found")
                    return None
            else:
                logger.error("user_id not found in token payload")
                return None
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.error(f"Token validation error: {e}")
            return None
    else:
        logger.error("Authorization header missing or malformed")
    return None

def validate_token(request):
    """Check if a valid token is provided in the request"""
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.split(' ', 1)[1]
        try:
            jwt.decode(token, secret, algorithms=[algorithm], issuer="gutopro")
            return True
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            return False
        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            return False
    return False
