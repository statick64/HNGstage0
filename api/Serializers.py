from .models import User
from rest_framework import serializers

# Model user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    

    