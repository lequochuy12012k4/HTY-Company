from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    document = models.FileField(upload_to='documents', null = True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_documents', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
