class MyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-XSS-Protection'] = "0"
        response['Strict-Transport-Security'] = "max-age = 3600; includeSubDomains"
        response["Content-Security-Policy"] = "CSP Level 2"
        response["Set-Cookie"] = "Max-Age = 0;Secure; HttpOnly"
        return response

