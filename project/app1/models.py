from django.db import models

class MRIImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='mri_scans/')  # Use ImageField to handle image uploads
    username = models.CharField(max_length=255)  # Use CharField to store the username

    def _str_(self):
        return f"ID: {self.id}, Username: {self.username}"
