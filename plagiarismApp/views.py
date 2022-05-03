import os
from django.conf import settings
from django.shortcuts import render, redirect
from .models import File
from django.views.generic import TemplateView
from pdfminer.high_level import extract_text
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from .plagiarismdetector import Plagiarism

class Showfile(TemplateView):
    def get(self, request, **kwargs):
        print(request.method)
        return render(request, 'home.html')

    def post(self, request, **kwargs):
        if request.FILES:
            myfile = request.FILES["pdffile"]
            filename = request.FILES["pdffile"].name
            File.objects.create(Name=filename, filepath=myfile)
            Files = File.objects.all().values()
            data=[]

            if len(Files)>1:
                myCheck = Plagiarism(Files)
                data = list(myCheck.CheckForPlagiarism())
            return render(request, 'display.html', {"data": data})
        return redirect("/")

    def delete(self, request, **kwargs):
        print("the form")
        File.objects.all().delete()
        return redirect("/")


class FileResult(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'display.html')

