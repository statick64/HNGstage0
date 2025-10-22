# Sentence Analyzer API

An API for analyzing sentences and text strings with various properties, built with Django and Django REST Framework.

## Overview

This API allows you to:
- Create and store sentences/text strings
- Retrieve sentences by their exact value
- Delete sentences
- Filter sentences based on their properties
- Analyze sentences using natural language queries

Each sentence is analyzed automatically when created, with the following properties:
- Length (number of characters)
- Whether it's a palindrome
- Number of unique characters
- Word count
- SHA-256 hash
- Character frequency map

## Installation & Setup

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
```
git clone https://github.com/statick64/HNGstage0
```

2. Navigate to the project directory:
```
cd HNGstage0
```

3. Create and activate a virtual environment:
```
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Run database migrations:
```
python manage.py migrate
```

6. Start the development server:
```
python manage.py runserver
```

The local API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

### Main Endpoints

| Method | Endpoint                        | Description                                       |
|--------|--------------------------------|--------------------------------------------------|
| POST   | `/strings`                     | Create a new sentence                            |
| GET    | `/strings`                     | Filter sentences based on properties             |
| GET    | `/strings/{string_value}`      | Get a specific sentence by its value             |
| DELETE | `/strings/{string_value}`      | Delete a sentence by its value                   |
| GET    | `/strings/filter-by-natural-language` | Filter sentences using natural language query |

### Creating a Sentence (POST `/strings`)

Request body:
```json
{
  "value": "Your sentence or text string here"
}
```

Response:
```json
{
  "id": "hash_value",
  "value": "Your sentence or text string here",
  "properties": {
    "length": 30,
    "is_palindrome": false,
    "unique_characters": 15,
    "word_count": 5,
    "sha256_hash": "hash_string",
    "character_frequency_map": {"a": 2, "b": 1, ...}
  },
  "created_at": "2025-10-22T04:22:38+01:00"
}
```

### Filtering Sentences (GET `/strings?param=value`)

Available query parameters:
- `is_palindrome`: Filter by palindrome status (true/false)
- `min_length`: Filter by minimum length
- `max_length`: Filter by maximum length
- `word_count`: Filter by exact word count
- `contains_character`: Filter by containing specific character

### Natural Language Filtering (GET `/strings/filter-by-natural-language?query=text`)

Example queries:
- "all palindromic strings"
- "all single word strings"
- "strings with 5 words"
- "short strings that contain character 'a'"


## Tech Stack

- Python 3.x
- Django 5.2.7
- Django REST Framework 3.16.1
- SQLite (development) / PostgreSQL (production)
- Gunicorn (for production deployment)
- Whitenoise (for static files)

## Testing

You can test the API using tools like cURL, Postman, or directly through your browser for GET requests.

Example cURL commands:

```bash
# Create a new sentence
curl -X POST -H "Content-Type: application/json" -d '{"value": "racecar"}' https://enchanting-eagerness-production.up.railway.appstrings

# Get sentence
curl "https://enchanting-eagerness-production.up.railway.app/strings/{string_value}"

# Delete sentence
curl "https://enchanting-eagerness-production.up.railway.app/strings/{string_value}"

# filtering sentence
curl "https://enchanting-eagerness-production.up.railway.app/strings?is_palindrome=false&min_length=5&max_length=400&word_count=3&contains_character=a"

# Use natural language filtering
curl "https://enchanting-eagerness-production.up.railway.app/strings/filter-by-natural-language?query=all palindrome strings"
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:
```
SECRET_KEY=your_secret_key_here
```

For security reasons, never commit your `.env` file to version control.