from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required

# Rate limit: 5 requests/minute for anonymous users
@ratelimit(key='ip', rate='5/m', block=True)
def login_view(request):
    """Simulates a login endpoint protected by rate limiting."""
    return JsonResponse({"message": "Login attempt recorded."})

# Optional: 10 requests/minute for authenticated users
@login_required
@ratelimit(key='user_or_ip', rate='10/m', block=True)
def dashboard_view(request):
    """Example of a protected page with user rate limit."""
    return JsonResponse({"message": "Authenticated access successful"})
