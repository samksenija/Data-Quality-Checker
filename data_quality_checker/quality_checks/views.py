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

            null_field_data = check_for_null_fields(df)

            return render(request, "results.html", {"null_field_data": null_field_data})
    except:
        print('redirect & present the error')  #TODO

    return render(request, "file_upload.html", {})

def check_for_null_fields(df):
    df_is_null = df.isnull()

    null_counts = df_is_null.sum()
    rows, cols = np.where(df_is_null)

    return [rows, cols, null_counts.to_dict()]