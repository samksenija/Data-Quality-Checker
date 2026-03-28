import io
import pandas as pd
import numpy as np

from django.shortcuts import render

def file_upload(request):
    try:
        if request.method == "POST" and request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']

            data = csv_file.read().decode('utf-8')
            df = pd.read_csv(io.StringIO(data))

            null_count_per_column = check_for_null_fields_count(df)

            return render(request, "results.html", 
                {"null_count_per_column": null_count_per_column})
    except:
        return render(request, "error_page.html", {})

    return render(request, "file_upload.html", {})

def check_for_null_fields_count(df):
    df_is_null = df.isnull()

    null_counts = df_is_null.sum()

    return null_counts.to_dict()

def check_for_null_fields_index_column(df):
    df_is_null = df.isnull()
    array_of_textual_result = []

    rows, cols = np.where(df_is_null)

    for r, c in zip(rows, cols):
        found_at = f"Null found at Row Index: {df.index[r]}, Column: {df.columns[c]}"
        array_of_textual_result.append(found_at)

    return array_of_textual_result