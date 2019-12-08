from django.db import models
from django.contrib.auth.models import User


class DocumentGroup(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Document(models.Model):
    name = models.CharField(max_length=255)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='%Y/%m/%d/')
    document_group = models.ForeignKey(DocumentGroup, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.name}'

