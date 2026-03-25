from django.utils.deprecation import MiddlewareMixin

class TenantMiddleware(MiddlewareMixin):
    """Middleware to set tenant organization for each request"""
    
    def process_request(self, request):
        request.current_organization = None
        if request.user.is_authenticated:
            request.current_organization = request.user.organization