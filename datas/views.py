from django.shortcuts import render
from . import applications

# app = applications.Application('base')
app = applications.App('base')


def main_view(request):
    html_view = 'datas/main.html'
    context = app.main(request)
    return render(request, html_view, context)


def ifs_view(request):
    html_view = 'datas/ifs.html'
    return render(request, html_view)
