from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Link(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="links")
    name = models.CharField(max_length=256)
    suffix = models.SlugField()
    url = models.URLField()
    limit = models.IntegerField(default=0)
    visit = models.IntegerField(default=0)
    qrcode = models.ImageField(upload_to="qrcodes", null=True)

    def __str__(self) -> str:
        return self.name
    


class Feedback(models.Model):

    name = models.CharField(max_length=256, null=False, blank=False)
    email = models.EmailField(null=False)
    message = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name

