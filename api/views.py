import re
import requests
from rest_framework.response import Response
from rest_framework import status, generics
from django.db import IntegrityError
from urllib.parse import unquote



from .models import Sentence, Properties
from .Serializers import SentenceSerializer , PropertiesSerializer



    

class SentencePostAndFilterView(generics.ListCreateAPIView):
    
    serializer_class = SentenceSerializer
    
    def post(self, request, *args, **kwargs):
        value = request.data.get("value")

        # Validate that 'value' is provided
        if not value:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )


        
        if not isinstance(value, str):
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY 
            )
        
        
        # Pass only the 'value' since model auto-hashes the id
        serializer = self.get_serializer(data={"value": value})
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST  # 404 for validation errors
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
            # Return a message 
            return Response(
                {
                    "message": "Sentence already exists.",
                },
                status=status.HTTP_409_CONFLICT
            )
    
    
    def get(self, request, *args, **kwargs):
        # Get query parameters
        is_palindrome = request.query_params.get("is_palindrome")
        min_length = request.query_params.get("min_length")
        max_length = request.query_params.get("max_length")
        word_count = request.query_params.get("word_count")
        contains_character = request.query_params.get("contains_character")

        # Start with all properties
        queryset = Properties.objects.select_related("sentence").all()
        

        # Apply filters dynamically
        if is_palindrome is not None:
            if is_palindrome.lower() in ["true", "1", "yes"]:
                queryset = queryset.filter(is_palindrome=True)
            elif is_palindrome.lower() in ["false", "0", "no"]:
                queryset = queryset.filter(is_palindrome=False)

        if min_length:
            queryset = queryset.filter(length__gte=int(min_length))

        if max_length:
            queryset = queryset.filter(length__lte=int(max_length))

        if word_count:
            queryset = queryset.filter(word_count=int(word_count))

        if contains_character:
            queryset = queryset.filter(sentence__value__icontains=contains_character)
            
        if not queryset:
            return Response(
                {"error": "Please provide a query parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # getting filters used
        filters_applied = {
            "is_palindrome": is_palindrome,
            "min_length": min_length,
            "max_length": max_length,
            "word_count": word_count,
            "contains_character": contains_character,
        }

        # Serialize the results
        results = []
        for prop in queryset:
            sentence_data = SentenceSerializer(prop.sentence).data
            properties_data = PropertiesSerializer(prop).data
            results.append({
                "id": sentence_data["id"],
                "value": sentence_data["value"],
                "properties": {
                    "length": properties_data.get("length"),
                    "is_palindrome": properties_data.get("is_palindrome"),
                    "unique_characters": properties_data.get("unique_characters"),
                    "word_count": properties_data.get("word_count"),
                    "sha256_hash": properties_data.get("sha256_hash"),
                    "character_frequency_map": properties_data.get("character_frequency_map")
                },
                "created_at": sentence_data["created_at"]
            })

        if not results:
            return Response(
                {"message": "No sentences found matching the provided filters."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
                            "data":results,
                            "count": len(results),
                            "filters_applied": filters_applied,
                        }, 
                        status=status.HTTP_200_OK)


    



class SentenceGetAndDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = SentenceSerializer
    
    def get(self, request, string_value, *args, **kwargs):
        # Ensure the parameter is a string

        try:
            # Retrieve the Sentence
            sentence = Sentence.objects.get(value=string_value)
            sentence_data = SentenceSerializer(sentence).data

            # Retrieve the Properties
            try:
                properties = Properties.objects.get(sentence=sentence)
                properties_data = PropertiesSerializer(properties).data
            except Properties.DoesNotExist:
                properties_data = None

            return Response(
                {
                    "id": sentence_data["id"],
                    "value": sentence_data["value"],
                    "properties": {
                        "length": properties_data.get("length"),
                        "is_palindrome": properties_data.get("is_palindrome"),
                        "unique_characters": properties_data.get("unique_characters"),
                        "word_count": properties_data.get("word_count"),
                        "sha256_hash": properties_data.get("sha256_hash"),
                        "character_frequency_map": properties_data.get("character_frequency_map")
                    },
                    "created_at": sentence_data["created_at"],
                },  
                status=status.HTTP_200_OK
            )

        except Sentence.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
            
            
    def delete(self, request, string_value, *args, **kwargs):
        # Decode URL-encoded values 
        decoded_value = unquote(string_value).strip()

        try:
            sentence = Sentence.objects.get(value=decoded_value)
            sentence.delete()  # Automatically deletes related Properties via CASCADE

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        except Sentence.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


        
        
class SentenceNaturalLanguageFilterView(generics.ListAPIView):
    serializer_class = SentenceSerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("query", "").lower().strip()

        if not query:
            return Response(
                {"error": "Please provide a query parameter, e.g. ?query=all single word palindromic strings"},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = Properties.objects.select_related("sentence").all()
        filters = {}
        contains_character = None
        conflicts = []

        # === Natural Language & Regex Parsing ===
        # Palindromic
        if re.search(r"\bpalindrome|palindromic\b", query):
            filters["is_palindrome"] = True

        # Word count: single vs multiple
        if re.search(r"\bsingle\s+word|one\s+word\b", query):
            filters["word_count"] = 1
        if re.search(r"\bmultiple\s+words|multi\s+word\b", query):
            if "word_count" in filters and filters["word_count"] == 1:
                conflicts.append("Cannot filter both single-word and multi-word strings.")
            filters["word_count__gt"] = 1

        # Length constraints
        longer_match = re.search(r"longer\s+than\s+(\d+)", query)
        shorter_match = re.search(r"shorter\s+than\s+(\d+)", query)

        if longer_match:
            filters["min_length"] = int(longer_match.group(1)) + 1
        if shorter_match:
            filters["max_length"] = int(shorter_match.group(1)) - 1

        # Detect general adjectives
        if "short" in query and "max_length" not in filters:
            filters["max_length"] = 5
        if "long" in query and "min_length" not in filters:
            filters["min_length"] = 10

        # Conflict: overlapping length constraints
        if "min_length" in filters and "max_length" in filters:
            if filters["min_length"] > filters["max_length"]:
                conflicts.append("Minimum length is greater than maximum length (invalid range).")

        # Character-based
        match = re.search(r"contain(?:s|ing)?(?:\s+the\s+letter)?\s+['\"]?([a-zA-Z])['\"]?", query)
        if match:
            contains_character = match.group(1).lower()
            filters["contains_character"] = contains_character

        # First vowel rule
        if re.search(r"contain(?:s|ing)?\s+(the\s+)?first\s+vowel", query):
            if contains_character and contains_character != "a":
                conflicts.append("Conflicting contains_character filters (letter vs first vowel).")
            contains_character = "a"
            filters["contains_character"] = "a"

        # "All strings" → no filter
        if query.strip() in ["all", "all strings"]:
            filters["no_filter"] = True

        # === Handle Conflicts ===
        if conflicts:
            return Response(
                {
                    "error": "Query parsed but resulted in conflicting filters.",
                    "details": conflicts,
                    "interpreted_query": {
                        "original": query,
                        "parsed_filters": filters
                    }
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # === Apply Filters ===
        if "is_palindrome" in filters:
            queryset = queryset.filter(is_palindrome=filters["is_palindrome"])
        if "word_count" in filters:
            queryset = queryset.filter(word_count=filters["word_count"])
        if "word_count__gt" in filters:
            queryset = queryset.filter(word_count__gt=filters["word_count__gt"])
        if "min_length" in filters:
            queryset = queryset.filter(length__gte=filters["min_length"])
        if "max_length" in filters:
            queryset = queryset.filter(length__lte=filters["max_length"])
        if contains_character:
            queryset = queryset.filter(sentence__value__icontains=contains_character)

        # === Build Response Data ===
        results = []
        for prop in queryset:
            sentence_data = SentenceSerializer(prop.sentence).data
            properties_data = PropertiesSerializer(prop).data
            results.append({
                "id": sentence_data["id"],
                "value": sentence_data["value"],
                "properties": {
                    "length": properties_data.get("length"),
                    "is_palindrome": properties_data.get("is_palindrome"),
                    "unique_characters": properties_data.get("unique_characters"),
                    "word_count": properties_data.get("word_count"),
                    "sha256_hash": properties_data.get("sha256_hash"),
                    "character_frequency_map": properties_data.get("character_frequency_map")
                },
                "created_at": sentence_data["created_at"]
            })

        # No matches
        if not results:
            return Response(
                {"message": "No sentences found matching the natural language query."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Final Response
        return Response({
            "data": results,
            "count": len(results),
            "interpreted_query": {
                "original": query,
                "parsed_filters": filters
            }
        }, status=status.HTTP_200_OK)
