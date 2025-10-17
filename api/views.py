import requests
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone
from rest_framework.decorators import api_view

from .models import User
from .Serializers import UserSerializer



@api_view(['GET'])
def getData(request):
    try:
        user = User.objects.first() # Getting the first users from the database
        if not user:
            return Response({"status": "error", "message": "No users available"}, status=404)  # error hadling if there are no users available 
        serializer = UserSerializer(user, many=False) # Serializes the user data
        cat_fact_request = requests.get("https://catfact.ninja/fact")  
        cat_fact = cat_fact_request.json().get('fact', 'unable to get cat fact')  # Gets a random cat fact
        context = {  # Creates the json response
            'status': 'success',
            'user': serializer.data,
            "timestamp": datetime.now(timezone.utc).isoformat(), # datetime in Iso format
            'fact': cat_fact, 

        }
        return Response(context)
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500) # Error handling
    



