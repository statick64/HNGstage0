from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import User
from .Serializers import UserSerializer


@api_view(['GET'])
def getData(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    data = {"status": "success"}
    return Response(serializer.data, data, status=status.HTTP_200_OK)
    



