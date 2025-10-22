# def count_char_frequency(input_string):
#     char_frequency = {}
#     for char in input_string:
#         if char in char_frequency:
#             char_frequency[char] += 1
#         else:
#             char_frequency[char] = 1
#     return char_frequency


# s = "hello world"
# frequency = count_char_frequency(s)
# print(frequency)


# import hashlib
# string_to_hash = "Hello, goom!"
# sha256_hash = hashlib.sha256(string_to_hash.encode()).hexdigest()
# print(sha256_hash)

# def is_palindrome_slice(text):
#     cleaned_text = text.lower().replace(" ", "")
#     return cleaned_text == cleaned_text[::-1]

# def is_palindrome(input_string):

#     # Remove spaces and convert to lowercase for case-insensitive comparison
#     cleaned_string = "".join(char for char in input_string if char.isalnum()).lower()
    
#     # Compare the cleaned string with its reverse
#     return cleaned_string == cleaned_string[::-1]


# def count_unique_characters(input_string):
#   unique_chars_set = set(input_string)
#   return len(unique_chars_set)

# # Example usage
# my_string = "hello world"
# unique_count = count_unique_characters(my_string)
# print(f"The number of unique characters in '{my_string}' is: {unique_count}")

# def word_counter(value):
#     words = value.split()
#     word_count = len(words)
#     print(f"The word count is: {word_count}")
    
    
# sentence = "Python"
# word_counter(sentence)

# print (is_palindrome("A man, a plan, a canal: Panama"))

loop = 1234
str_loop = str(loop)

print(f"this is th{len(str_loop)} {loop}")