import io
import pandas as pd
import numpy as np

from .forms import ColumnMappingForm
from django.shortcuts import render
from fpdf import FPDF

df = None
duplicate_rows = None

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
        
        if request.method == "POST":
            form = ColumnMappingForm(request.POST, columns=duplicate_rows["headers"], data_types=data_types)

            if form.is_valid():
                show_schema_results = True
                schema_result = schema_check_datatypes(df, form.cleaned_data.items())

            context = {"null_count_per_column": null_count_per_column,
                "duplicate_rows": duplicate_rows,
                "show_schema_results": show_schema_results,
                "schema_check_datatypes": schema_result}

        return render(request, "results.html", context)
                        
    except:
        return render(request, "error_page.html", {})


def null_value_details(request):
    try:
        null_value_details = check_for_null_fields_index_column(df)
        return render(request, "null_value_details.html", 
            {"null_value_details": null_value_details})
    except:
        return render(request, "error_page.html", {})
    

def check_for_null_fields_count(df):
    df_is_null = df.isnull()

    null_counts = df_is_null.sum()

    return null_counts.to_dict()

def check_for_null_fields_index_column(df):
    df_is_null = df.isnull()
    array_of_textual_result = []

    rows, cols = np.where(df_is_null)

    for r, c in zip(rows, cols):
        found_at = f"Null found at row index: {df.index[r] + 1}, column: {df.columns[c]}"
        array_of_textual_result.append(found_at)

    return array_of_textual_result

def check_for_duplicate_rows(df):
    duplicate_rows = df[df.duplicated()]
    
    context = {
        "headers": duplicate_rows.columns.tolist(),
        "duplicate_rows": duplicate_rows.values.tolist(),
        "duplicate_count": len(duplicate_rows),
    }

    return context

def check_for_which_columns_schema_needs_to_be_validated(column_mappings):
    column_mappings = [(column, value) for column, value in column_mappings if value != ""]

    return column_mappings

def schema_check_datatypes(df, column_mappings):
    columns_to_be_validates_for_data_type = check_for_which_columns_schema_needs_to_be_validated(column_mappings)
    datatype_conversion_results = []

    for column, data_type in columns_to_be_validates_for_data_type:
        try:
            df[column].astype(data_type)
            validation_result = "Valid"

        except ValueError:
            validation_result = "Invalid"

        validation = {
            "column_name": column,
            "expected_type": data_type,
            "validation_result": validation_result
        }
        
        datatype_conversion_results.append(validation)
  
    return datatype_conversion_results

def generate_pdf(context):
    pass