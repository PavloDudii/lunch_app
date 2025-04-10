

class VersionControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        app_version = request.headers.get('X-App-Version', '0.0.0')
        request.app_version = app_version
        response = self.get_response(request)
        return response
