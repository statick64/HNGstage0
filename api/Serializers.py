from .models import Sentence, Properties
from rest_framework import serializers
import hashlib

# Model user serializer
class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = '__all__'
        read_only_fields = ('created_at', 'id')
    
    # def validate_value(self, value):
    #     if not isinstance(value, str):
    #         raise serializers.ValidationError("The 'value' field must be a string.")
    #     return value
    
         
        
        
    

class PropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Properties
        fields = '__all__'
    