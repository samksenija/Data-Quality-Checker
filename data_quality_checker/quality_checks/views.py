import io
import pandas as pd
import numpy as np

from django.shortcuts import render

df = None

def file_upload(request):
    try:
        if request.method == "POST" and request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']

            data = csv_file.read().decode('utf-8')

            global df 
            df = pd.read_csv(io.StringIO(data))

            null_count_per_column = check_for_null_fields_count(df)
            duplicate_rows = check_for_duplicate_rows(df)

            return render(request, "results.html", 
                {"null_count_per_column": null_count_per_column,
                "duplicate_rows": duplicate_rows})
    except:
        return render(request, "error_page.html", {})

    return render(request, "file_upload.html", {})


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