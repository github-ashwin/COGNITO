from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',    # To get all the rooms
        'GET /api/rooms/:id' # To get a specific room 
    ]
    return Response(routes)