from django.forms import ModelForm, Form
from django import forms
from .models import Document, DocumentGroup
from django.contrib.auth.models import User


class UploadDocumentForm(ModelForm):
     class Meta:
         model = Document
         fields = ['name', 'user', 'file', 'document_group']


class AddDocumentGroupForm(ModelForm):
    class Meta:
        model = DocumentGroup
        fields = ['name', 'user']


class LoginForm(Form):
        username = forms.CharField()
        password = forms.CharField(max_length=32, widget=forms.PasswordInput)