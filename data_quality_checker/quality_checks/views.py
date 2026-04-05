import io
import os
import pandas as pd

from django.conf import settings
from .forms import ColumnMappingForm
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .utils import check_for_null_fields_count, check_for_null_fields_index_column, check_for_duplicate_rows, schema_check_datatypes, generate_pdf, results_context 

df = None
duplicate_rows = None
result_of_validation = None

global data_types
data_types = {
    "": "",
    "Integer": "int",
    "Float": "float",
    "Complex": "complex",
    "Boolean": "bool",
    "String": "str",
    "Bytes": "bytes",
    "ByteArray": "bytearray",
    "List": "list",
    "Tuple": "tuple",
    "Set": "set",
    "Dictionary": "dict",
    "Null": "none"
}

def file_upload(request):
    try:
        if request.method == "POST" and request.FILES.get('csv_file'):
            global df
            
            csv_file = request.FILES['csv_file']
            csv_file_name =  csv_file.name
    
            if csv_file_name.endswith('.csv'):
                data = csv_file.read().decode('utf-8')
                df = pd.read_csv(io.StringIO(data))
            elif csv_file_name.endswith('.xlsx'):
                df = pd.read_excel(csv_file)
            elif csv_file_name.endswith('.xls'):
                df = pd.read_excel(csv_file, engine='xlrd')

            global duplicate_rows
            duplicate_rows = check_for_duplicate_rows(df)
            
            columns = duplicate_rows["headers"]
            columns = [str(item) for item in duplicate_rows["headers"]]

            form = ColumnMappingForm(request.POST, columns=columns, data_types=data_types)

            return render(request, "schema_validation.html", {
                "columns": columns,
                "data_types": data_types,
                "form": form
            })
    except:
        return render(request, "error_page.html", {})

    return render(request, "file_upload.html", {})


def results(request):
    try:
        show_schema_results = False
        null_count_per_column = check_for_null_fields_count(df)
        schema_result = []
        
        global result_of_validation
        result_of_validation = results_context(null_count_per_column, duplicate_rows, show_schema_results, schema_result)
        
        if request.method == "POST":
            form = ColumnMappingForm(request.POST, columns=duplicate_rows["headers"], data_types=data_types)

            if form.is_valid():
                show_schema_results = True
                schema_result = schema_check_datatypes(df, form.cleaned_data.items())

                result_of_validation = results_context(null_count_per_column, duplicate_rows, show_schema_results, schema_result)
                
        return render(request, "results.html", result_of_validation)              
    except:
        return render(request, "error_page.html", {})


def null_value_details(request):
    try:
        null_value_details = check_for_null_fields_index_column(df)
        return render(request, "null_value_details.html", 
            {"null_value_details": null_value_details})
    except:
        return render(request, "error_page.html", {})
    

def download_pdf(request):
    try:
        null_value_details = check_for_null_fields_index_column(df)
        result_of_validation['null_value_details'] = null_value_details
        
        validation_reports_path = settings.BASE_DIR / "validation_reports"
        validation_reports_path.mkdir(parents=True, exist_ok=True)
        
        filename = 'validation-result-' + datetime.today().strftime("%Y-%m-%d") + '-' + datetime.now().strftime("%H-%M-%S") + '.pdf'
        file_path = str(validation_reports_path / filename)
        
        buffer = io.BytesIO()

        generate_pdf(file_path, result_of_validation)

        pdf = buffer.getvalue()
        buffer.close()

        pdf = open(file_path, 'rb')
        response = HttpResponse(pdf.read())
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response
    except:
        return render(request, "error_page.html", {})