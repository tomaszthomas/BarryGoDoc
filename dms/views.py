from django.shortcuts import render
from django.views.generic import ListView, FormView, View
from .models import DocumentGroup, Document
from .forms import UploadDocumentForm, AddDocumentGroupForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.contrib.auth.models import User
import mimetypes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin



class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dms/about.html')


class ListDocumentGroups(LoginRequiredMixin, ListView):
    model = DocumentGroup
    login_url = reverse_lazy('user-login')
    redirect_field_name = reverse_lazy('user-login')


class ListDocuments(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('user-login')
    redirect_field_name = reverse_lazy('user-login')
    model = DocumentGroup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    login_url = reverse_lazy('user-login')
    redirect_field_name = reverse_lazy('user-login')

    def post(self, request, pk):

            document = Document.objects.get(pk=pk)
            document.delete()
            # return redirect(reverse('document-list', kwargs={'pk': document.id}))
            return redirect(reverse('document-group-list'))


class DocumentGroupAddView(LoginRequiredMixin, FormView):
    template_name = 'dms/document_group_add.html'
    form_class = AddDocumentGroupForm
    login_url = reverse_lazy('user-login')
    redirect_field_name = reverse_lazy('user-login')

    def post(self, request):
        form = AddDocumentGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('document-group-list'))


class UploadDocumentView(LoginRequiredMixin, FormView):
    template_name = 'dms/upload_document.html'
    form_class = UploadDocumentForm
    login_url = reverse_lazy('user-login')
    redirect_field_name = reverse_lazy('user-login')

    def post(self, request):
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            return redirect(reverse('document-list', kwargs={'pk': document.document_group.id}))


class PreviewDocumentView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user-login')
    redirect_field_name = reverse_lazy('user-login')

    def get(self, request, id):
        document = Document.objects.get(pk=id)
        file = document.file.open()

        response = HttpResponse(content=file)
        response['Content-Type'] = mimetypes.guess_type(document.file.name)[0]
        return response


class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def form_valid(self, form):
        import pdb; pdb.set_trace()
        User.objects.create_user(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            username=form.cleaned_data['username'],
        )
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    login_url = reverse_lazy('user-login')
    redirect_field_name = reverse_lazy('user-login')

    def post(self, request, pk):

            user = User.objects.get(pk=pk)
            user.delete()
            # return redirect(reverse('document-list', kwargs={'pk': document.id}))
            return redirect(reverse('users-list'))

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('users-list')


class ListUsers(LoginRequiredMixin, ListView):
    model = User
    login_url = reverse_lazy('user-login')
    redirect_field_name = reverse_lazy('user-login')


class LoginView(FormView):
    template_name = "auth/user_login.html"
    form_class = LoginForm
    success_url = reverse_lazy('document-group-list')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            messages.info(self.request, "Logged in")
            return super().form_valid(form)
        else:
            messages.error(self.request, "incorrect email or password")
            return redirect(reverse('user-login'))


@login_required(login_url="/user-login/")
def logoutUser(request):
    messages.info(request, "Logged out")
    logout(request)
    return redirect("about")


