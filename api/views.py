from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
import sys


# Create your views here.

def index(request):
    print(suspect_person_detail)
    return HttpResponse("Pakistan zindabad")

# def get_report(request)
