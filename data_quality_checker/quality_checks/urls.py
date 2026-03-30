from django.urls import path

from . import views

urlpatterns = [
    path("", views.file_upload, name="index_file_upload"),
    path("file_upload", views.file_upload, name="file_upload"),
    path("null-value-details", views.null_value_details, name="null_value_details"),
    path("results", views.results, name="results"),
]