from django.urls import path

from . import views

urlpatterns = [
    path("", views.file_upload, name="index_file_upload"),
    path("results", views.file_upload, name="results"),
    path("null-value-details", views.null_value_details, name="null_value_details")

]