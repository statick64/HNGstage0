import requests
from rest_framework.response import Response
from rest_framework import status, generics
from django.db import IntegrityError
from datetime import datetime, timezone
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import hashlib

from .models import Sentence, Properties
from .Serializers import SentenceSerializer , PropertiesSerializer



    

class SentenceView(generics.CreateAPIView):
    
    serializer_class = SentenceSerializer
    
    def create(self, request, *args, **kwargs):
        value = request.data.get("value")

        # Validate that 'value' is provided
        if not value:
            return Response(
                {"error": "The 'value' field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )


        
        # Pass only the 'value' since model auto-hashes the id
        serializer = self.get_serializer(data={"value": value})
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY  # 422 for validation errors
            )
        
        try:
            # self.perform_create(serializer)
            sentence = serializer.save()
            
            # Create or update its Properties
            properties, _ = Properties.objects.get_or_create(sentence=sentence)
            properties.save()  # triggers automatic computation from model.save()
            properties_data = PropertiesSerializer(properties).data

            return Response(
                {
                    "id": serializer.data["id"],
                    "value": serializer.data["value"],
                    "properties": {
                        "length": properties_data.get("length"),
                        "is_palindrome": properties_data.get("is_palindrome"),
                        "unique_characters": properties_data.get("unique_characters"),
                        "word_count": properties_data.get("word_count"),
                        "sha256_hash": properties_data.get("sha256_hash"),
                        "character_frequency_map": properties_data.get("character_frequency_map")
                    },
                    "created_at": serializer.data["created_at"],},
                status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            # Return the existing sentence instead of failing
            existing_sentence = Sentence.objects.get(value=value)
            existing_data = SentenceSerializer(existing_sentence).data
            return Response(
                {
                    "message": "Sentence already exists.",
                },
                status=status.HTTP_409_CONFLICT
            )

