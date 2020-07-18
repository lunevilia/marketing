from django.shortcuts import render
from category.models import *
# Create your views here.
def main_show(request):
    show_all = Category.objects.all()
    return render(request, "main.html", {'show_all':show_all,})