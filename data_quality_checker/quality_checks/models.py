from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class File_Data(models.Model):
    UPLOADED = 'Uploaded'
    DELETED = 'Deleted'
    CATEGORY_CHOICES = [
        (UPLOADED, 'Uploaded'),
        (DELETED, 'Deleted')
    ]
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_id')
    file_id = models.AutoField(primary_key=True)
    row_number= models.IntegerField(null = True)
    original_file_name = models.CharField(max_length=50)
    file_name = models.CharField(max_length=50, null=True)
    file_path = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=UPLOADED)
    uploaded_at = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return f"{self.pk} by user {self.user}, file name: {self.original_file_name}, time: {self.uploaded_at}"
