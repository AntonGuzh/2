from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, FileResponse
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AuthUserForm, RegisterUserForm, CreateCV
from .models import CVModel

import jinja2
import os
import subprocess

class MyLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('list_page')

    def get_success_url(self):
        return self.success_url


class MyRegisterView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('list_page')


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('list_page')


class RedactorView(CreateView, LoginRequiredMixin):
    model = CVModel
    form_class = CreateCV
    template_name = 'redactor.html'
    success_url = reverse_lazy('list_page')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


def MyListView(request):
    models = []
    if request.user.is_authenticated:
        models = CVModel.objects.filter(owner=request.user)
    return render(request, 'list.html', {'models': models})


def DownloadView(request, id):
    if not request.user.is_authenticated:
        return render(request, '403.html')
    model = CVModel.objects.filter(owner=request.user, id=id)
    if not model:
        return render(request, '403.html')
    model = model[0]

    latex_jinja_env = jinja2.Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath('.'))
    )
    template = latex_jinja_env.get_template('main_app/templates/cv.tex')
    cv = template.render({'m': model})
    with open('cv_res.tex', 'w', encoding='utf-8') as f:
        f.write(cv)
    code = subprocess.call(['latexmk', 'cv_res.tex'])
    if code:
        return HttpResponse('<h1>Простите, что-то пошло не так</h1>')

    file = FileResponse(open('cv_res.pdf', 'rb'), content_type='application/pdf')
    clear()
    return file


class DeleteCvView(DeleteView, LoginRequiredMixin):
    model = CVModel
    template_name = 'list.html'
    success_url = reverse_lazy('list_page')


class UpdateCvView(UpdateView, LoginRequiredMixin):
    model = CVModel
    form_class = CreateCV
    template_name = 'redactor.html'
    success_url = reverse_lazy('list_page')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


def clear():
    for file in os.listdir('./'):
        if file.startswith('cv_res') and not file.endswith('.pdf'):
            os.remove(file)
    for file in os.listdir('./'):
        if file.endswith('.png') or file.endswith('.jpg'):
            os.remove(file)
