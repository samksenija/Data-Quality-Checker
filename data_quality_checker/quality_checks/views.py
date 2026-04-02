import io
import pandas as pd

from .forms import ColumnMappingForm
from django.shortcuts import render
from .utils import check_for_null_fields_count, check_for_null_fields_index_column, check_for_duplicate_rows, schema_check_datatypes, generate_pdf 

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
            csv_file = request.FILES['csv_file']

            data = csv_file.read().decode('utf-8')

            global df 
            df = pd.read_csv(io.StringIO(data))

            global duplicate_rows
            duplicate_rows = check_for_duplicate_rows(df)
            columns = duplicate_rows["headers"]

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
        
        if request.method == "POST":
            form = ColumnMappingForm(request.POST, columns=duplicate_rows["headers"], data_types=data_types)

            if form.is_valid():
                show_schema_results = True
                schema_result = schema_check_datatypes(df, form.cleaned_data.items())

            result_of_validation = {"null_count_per_column": null_count_per_column,
                "duplicate_rows": duplicate_rows,
                "show_schema_results": show_schema_results,
                "schema_check_datatypes": schema_result}

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
    


