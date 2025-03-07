# CSV Processing App

A Django-based web application that processes CSV files asynchronously using Celery and Redis.

## Features
- Upload CSV files and process data asynchronously
- Calculate total revenue, average discount, and best-selling products
- Search functionality for filtering products
- Uses Celery and Redis for background tasks

## Installation

### Prerequisites
- Python 3.9+
- Redis Server
- Django
- Celery
- Pandas

### Setup

1. Clone the repository:
   ```bash
   git clone your-repo-url
   cd csv-processing-app

2. Create a virtual environment and activate it:
  ```bash
  python -m venv venv
  venv\Scripts\activate

3. Install dependencies
  ```bash
  pip install -r requirements.txt

4. Run database migrations:
  ```bash
  python manage.py migrate

5. Start Redis (Ensure Redis is installed and running):
  ```bash
  redis-server

6. Start Celery:
  ```bash
  celery -A csv_processing.celery worker --pool=solo -l info

7. Run the Django server:
  ```bash
  python manage.py runserver

### Usage:

  Upload a CSV file
  View processed results (total sales, best-selling products, etc.)
  Use search to filter product data dynamically
"# csv-processing" 
