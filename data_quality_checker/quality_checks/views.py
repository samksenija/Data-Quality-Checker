import io
import pandas as pd

from django.shortcuts import render

def file_upload(request):
    try:
        if request.method == "POST" and request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']

            data = csv_file.read().decode('utf-8')
            df = pd.read_csv(io.StringIO(data))

            print(check_for_null_fields(df))
    except:
        print('redirect & present the error')  #TODO

    return render(request, "file_upload.html", {})

def check_for_null_fields(df):
    return df.isnull().sum()