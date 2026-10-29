# core/middleware.py
class JavaScriptCharsetMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.get('Content-Type') == 'application/javascript':
            response['Content-Type'] = 'application/javascript; charset=utf-8'
        return response