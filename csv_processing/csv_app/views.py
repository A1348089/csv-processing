from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
import pandas as pd
from django.contrib import messages
from .models import UploadedFile
from .tasks import process_csv

def upload_file(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
         # Validate file type
        if not file.name.endswith(".csv"):
            messages.error(request, "Only CSV files are allowed.")
            return render(request, "file_upload/upload.html")

        file_instance = UploadedFile.objects.create(file=file)
        summary = process_csv.delay(file_instance.id)

        df = pd.read_csv(file_instance.file.path)
        data = df.to_dict(orient='records')

        try:
            # Get the latest uploaded file
            latest_file = UploadedFile.objects.latest('uploaded_at')
            
            # Process the CSV using Celery (async task)
            result = process_csv(latest_file.id)

            return render(request, 'file_upload/table.html', {'data': data, 'stats': summary, 'result':result})
        
        except UploadedFile.DoesNotExist:
            return JsonResponse({'error': 'No file found'}, status=400)

    return render(request, 'file_upload/upload.html')


def search_product(request):
    if request.method == "POST":
        query = request.POST.get('product_name', '').lower()

        try:
            latest_file = UploadedFile.objects.latest('uploaded_at')
        except UploadedFile.DoesNotExist:
            return render(request, 'file_upload/table.html', {'data': [], 'error': 'No file found'})

        df = pd.read_csv(latest_file.file.path)

        # Convert DataFrame to list of dictionaries
        processed_data = df.to_dict(orient='records')

        # Filter based on product name
        filtered_data = [row for row in processed_data if query in str(row.get('Product Name', '')).lower()]

        try:
            # Get the latest uploaded file
            latest_file = UploadedFile.objects.latest('uploaded_at')
            
            # Process the CSV using Celery (async task)
            result = process_csv(latest_file.id)

            return render(request, 'file_upload/table.html', {'data': filtered_data, 'result':result})
        
        except UploadedFile.DoesNotExist:
            return JsonResponse({'error': 'No file found'}, status=400)
