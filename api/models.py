from django.db import models
import hashlib


# user model

class Sentence(models.Model):  
    id = models.CharField(max_length=200, primary_key=True)
    value = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.value
    
    
    def save(self, *args, **kwargs):
        # Automatically hash the value for the ID before saving
        if not self.id and self.value:
            self.id = hashlib.sha256(self.value.encode()).hexdigest()
        super().save(*args, **kwargs)
        
    



class Properties(models.Model):
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    length = models.IntegerField(default=0)
    is_palindrome = models.BooleanField()
    unique_characters = models.IntegerField()
    word_count = models.IntegerField()
    sha256_hash = models.CharField(max_length = 200)
    character_frequency_map = models.JSONField(default=dict)
    
    def character_frequency_count(self):
        char_frequency = {}
        for char in self.sentence.value:
            char_frequency[char] = char_frequency.get(char, 0) + 1
        self.character_frequency_map = char_frequency
        return char_frequency
    
    
    def is_palindrome_func(self):
        # Remove spaces and convert to lowercase for case-insensitive comparison
        cleaned_string = "".join(char for char in self.sentence.value if char.isalnum()).lower()
        
        # Compare the cleaned string with its reverse
        self.is_palindrome = cleaned_string == cleaned_string[::-1]


    def count_unique_characters(self):
        unique_chars_set = set(self.sentence.value)
        self.unique_characters = len(unique_chars_set)

    def word_counter(self):
        words = self.sentence.value.split()
        word_count = len(words)
        self.word_count = word_count
        
    def save(self, *args, **kwargs):
        # Automatically compute all properties before saving.
        self.length = len(self.sentence.value)
        self.is_palindrome_func()
        self.count_unique_characters()
        self.word_counter()
        self.character_frequency_count()
        self.sha256_hash = hashlib.sha256(self.sentence.value.encode()).hexdigest()
        super().save(*args, **kwargs)

