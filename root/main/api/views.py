from django.http import JsonResponse


def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',    # To get all the rooms
        'GET /api/rooms/:id' # To get a specific room 
    ]
    return JsonResponse(routes, safe=False)