import jwt
from django.conf import settings
from django.http import JsonResponse
from jwt.exceptions import InvalidTokenError
from functools import wraps

def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check for the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Authorization header is required"}, status=401)

        # The expected format is "Bearer <token>"
        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                return JsonResponse({"error": "Authorization header must start with 'Bearer'"}, status=401)
        except ValueError:
            return JsonResponse({"error": "Invalid Authorization header format"}, status=401)

        # Decode the JWT token
        try:
            decoded_token = jwt.decode(token, settings.HASURA_SECRET_KEY, algorithms=["ES256"])
            # Attach the decoded token to the request for access in views
            request.user_payload = decoded_token
        except InvalidTokenError:
            return JsonResponse({"error": "Invalid or expired token"}, status=401)

        # Proceed with the original view
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
