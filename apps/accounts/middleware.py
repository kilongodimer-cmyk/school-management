from django.utils.deprecation import MiddlewareMixin


class SchoolMiddleware(MiddlewareMixin):
    """Attach the user's school to the request object for convenience and basic scoping."""
    def process_request(self, request):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            request.school = getattr(user, 'school', None)
        else:
            request.school = None
