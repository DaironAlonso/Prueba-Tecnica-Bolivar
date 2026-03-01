from django.http import JsonResponse

API_KEY = '123456'

RUTAS_PROTEGIDAS = '/api/'

class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(RUTAS_PROTEGIDAS):
            key = request.headers.get('X-Api-Key') or request.headers.get('x-api-key')
            if key != API_KEY:
                return JsonResponse(
                    {'error': 'API key inválida o ausente'},
                    status=401
                )
        return self.get_response(request)
