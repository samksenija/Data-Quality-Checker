from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

def file_upload(request):
    return render(request, "file_upload.html", {})