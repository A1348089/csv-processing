from celery import shared_task
import pandas as pd
import os
from .models import UploadedFile

@shared_task
def process_csv(file_id):
    try:
        file_instance = UploadedFile.objects.get(id=file_id)

        if not os.path.exists(file_instance.file.path):
            return {'error': 'File does not exist'}

        df = pd.read_csv(file_instance.file.path)

        # Ensure required columns are present
        required_columns = {'Sales', 'Quantity', 'Discount', 'Profit', 'Product Name'}
        if not required_columns.issubset(df.columns):
            missing_cols = required_columns - set(df.columns)
            return {'error': f'Missing columns: {", ".join(missing_cols)}'}

        # Convert necessary columns to numeric (handling non-numeric values)
        for col in ['Sales', 'Quantity', 'Discount', 'Profit']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)  # Replace NaN with 0

        # Compute Metrics
        total_revenue = float(df['Sales'].sum())
        avg_discount = float(df['Discount'].mean())

        # Get Product Statistics
        best_selling_product = df.groupby('Product Name')['Quantity'].sum()
        most_profitable_product = df.groupby('Product Name')['Profit'].sum()

        best_selling_product = best_selling_product.idxmax() if not best_selling_product.empty else None
        most_profitable_product = most_profitable_product.idxmax() if not most_profitable_product.empty else None
        max_discount_product = df.loc[df['Discount'].idxmax(), 'Product Name'] if not df['Discount'].isna().all() else None

        # Additional Metrics
        sum_sales = float(df['Sales'].sum())
        sum_quantity = int(df['Quantity'].sum())
        sum_discount = float(df['Discount'].sum())
        sum_profit = float(df['Profit'].sum())

        avg_sales = float(df['Sales'].mean())
        avg_quantity = float(df['Quantity'].mean())
        avg_profit = float(df['Profit'].mean())

        count_records = int(df.shape[0])  # Total number of records

        return {
            'total_revenue': total_revenue,
            'avg_discount': avg_discount,
            'best_selling_product': best_selling_product,
            'most_profitable_product': most_profitable_product,
            'max_discount_product': max_discount_product,
            
            'sum_sales': sum_sales,
            'sum_quantity': sum_quantity,
            'sum_discount': sum_discount,
            'sum_profit': sum_profit,
            'avg_sales': avg_sales,
            'avg_quantity': avg_quantity,
            'avg_profit': avg_profit,
            'count_records': count_records
        }

    except Exception as e:
        return {'error': str(e)}