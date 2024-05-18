
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .models import UserModel

def generate_token(user):
    """Generate a token for a particular user after login"""
    access_token = AccessToken.for_user(user)
    refresh_token = RefreshToken.for_user(user)
    return {
        'access_token': str(access_token),
        'refresh_token': str(refresh_token),
    }

def get_user_from_request(request):
    """Retrieves a user from a token"""
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.split(' ', 1)[1]
        try:
            payload = AccessToken(token).payload
        except Exception:
            return None
        user_id = payload.get("user_id")
        user_type = payload.get("user_type")
        user = UserModel.objects.get(pk=user_id)
        return user
    return None

def validate_token(request):
    """Check if a token is passed within the request and if it starts with 'Bearer'"""
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        return True
    else:
        return False
