from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import User
import uuid
import os


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads/', new_name)

class FileType(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )
    def __str__(self):
        return self.name

class File(models.Model):
    FILE_TYPES = [
       ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('text', 'Text'),
        ('3d', '3D'),
    ]
    shared_with = models.ManyToManyField(
        User,
        blank=True,
        #through='SharedFile',
        related_name='shared_files'
    )
    file_type_fk = models.ForeignKey(
        FileType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    original_name = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name or self.file.name

class SharedFile(models.Model):

    file = models.ForeignKey(
        'File',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    shared_at = models.DateTimeField(
        auto_now_add=True
    )