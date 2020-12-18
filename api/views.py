from django.shortcuts import render, redirect
from .models import *
from backend_site.models import suspect_from_app_User, app_user, suspect_from_anonymous
from .serializers import *
from django.http import HttpResponse, JsonResponse
import sys

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import io
from django.core.files.storage import FileSystemStorage



def index(request):
    print(suspect_person_detail)
    return HttpResponse("Pakistan zindabad")

def getAllReport(request):
    data = suspect_person_detail.objects.all()
    serialize_data = serializer_suspectData(data, many=True) 
    return JsonResponse(serialize_data.data, safe=False)

def getReport(request, sid):
    data = suspect_person_detail.objects.get(id = sid)
    serialize_data = serializer_suspectData(data)
    return JsonResponse(serialize_data.data, safe=True)

@csrf_exempt
def uploadSuspect(request):
    data = {}
    if request.method == "POST":
        try: 
            data['user_id'] = app_user.objects.get(id=request.POST['user_id'])
            data['description'] = request.POST['description']
            suspect_video = request.FILES['suspect_video']

            fs = FileSystemStorage()
            uploaded_file = fs.save(suspect_video.name, suspect_video)

            data['video_url'] = fs.url(uploaded_file)

            obj = suspect_from_app_User(user_id=data['user_id'], description=data['description'], video_url=data['video_url'])
            obj.save()
            return JsonResponse({"msg": "Successfull upload"}, safe=True)
        except:
            return JsonResponse({"msg": "error"}, safe=True)

    else:
        return JsonResponse({"msg": "error: use post method"}, safe=True)


@csrf_exempt
def uploadSuspect_anonymous(request):
    data = {}
    if request.method == "POST":
        try: 
            data['description'] = request.POST['description']
            suspect_video = request.FILES['suspect_video']

            fs = FileSystemStorage()
            uploaded_file = fs.save(suspect_video.name, suspect_video)

            data['video_url'] = fs.url(uploaded_file)

            obj = suspect_from_anonymous(description=data['description'], video_url=data['video_url'])
            obj.save()
            return JsonResponse({"msg": "Successfull upload"}, safe=True)
        except:
            return JsonResponse({"msg": "error"}, safe=True)

    else:
        return JsonResponse({"msg": "error: use post method"}, safe=True)

        