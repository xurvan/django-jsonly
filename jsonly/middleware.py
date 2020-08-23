import json


class JsonMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        temp = dict()
        if request.body:
            temp = json.loads(request.body)
        request.json = temp

        return self.get_response(request)
