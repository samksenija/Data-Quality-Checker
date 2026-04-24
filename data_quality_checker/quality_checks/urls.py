from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("file_upload", views.file_upload, name="file_upload"),
    path("null-value-details", views.null_value_details, name="null_value_details"),
    path("results", views.results, name="results"),
    path("download_pdf", views.download_pdf, name="download_pdf"),
    path("archive", views.archive, name="archive"),
    path("delete_archive_element/<int:id>", views.delete_archive_element, name="delete_archive_element"),
    path("check_if_archive_data", views.check_if_archive_data, name="check_if_archive_data")
]