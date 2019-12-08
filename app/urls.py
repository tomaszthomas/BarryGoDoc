"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dms import views
from dms.views import logoutUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('document-group-list/', views.ListDocumentGroups.as_view(), name='document-group-list'),
    path('document-group-list/<pk>', views.ListDocuments.as_view(), name='document-list'),
    path('document-upload', views.UploadDocumentView.as_view(), name='upload-document'),
    path('document-preview/<id>', views.PreviewDocumentView.as_view(), name='document-preview'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('document-group-add/', views.DocumentGroupAddView.as_view(), name='document-group-add'),
    path('document-delete/<pk>', views.DocumentDeleteView.as_view(), name='document-delete'),
    path('user-create/', views.UserCreateView.as_view(), name='user-create'),
    path('users-list/', views.ListUsers.as_view(), name='users-list'),
    path('user-login', views.LoginView.as_view(), name='user-login'),
    path('user-logout', logoutUser, name='user-logout'),
    path('user-list/<pk>', views.UserUpdateView.as_view(), name='user-update'),
    path('user-delete/<pk>', views.UserDeleteView.as_view(), name='user-delete'),
]
