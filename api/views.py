from django.shortcuts import render, redirect
from .models import *
from backend_site.models import suspect_from_app_User, app_user, suspect_from_anonymous, caught_suspect
from .serializers import serializer_suspectData
from django.http import HttpResponse, JsonResponse
import sys
import ast
import base64
import numpy as np
import cv2
import random
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import io
from django.core.files.storage import FileSystemStorage



def check_api(request):
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
    if request.method == "POST":
        try: 
            app_user_instance = app_user.objects.get(id=request.POST['user_id'])
            suspect_video = request.FILES['suspect_video']
            fs = FileSystemStorage()
            uploaded_file = fs.save(suspect_video.name, suspect_video)
            obj = suspect_from_app_User(user_id=app_user_instance, description=request.POST['description'], video_url=fs.url(uploaded_file))
            obj.save()
            return JsonResponse({"response": "201 created"}, safe=True)
        except:
            return JsonResponse({"response": "403 Forbidden"}, safe=True)
    else:
        return JsonResponse({"response": "405 Method Not Allowed"}, safe=True)


@csrf_exempt
def uploadSuspect_anonymous(request):
    if request.method == "POST":
        try: 
            suspect_video = request.FILES['suspect_video']
            fs = FileSystemStorage()
            uploaded_file = fs.save(suspect_video.name, suspect_video)
            obj = suspect_from_anonymous(description=request.POST['description'], video_url=fs.url(uploaded_file))
            obj.save()
            return JsonResponse({"response": "201 created"}, safe=True)
        except:
            return JsonResponse({"response": "403 Forbidden"}, safe=True)

    else:
        return JsonResponse({"response": "405 Method Not Allowed"}, safe=True)


@csrf_exempt
def creat_app_user(request):
    if request.method == "POST":
        # try: 
        # stream = io.BytesIO(request.body)
        # python_data = JSONParser().parse(stream)
        print(request.POST)
        return JsonResponse({"response": "201 created"}, safe=True)
        # except:
        #     return JsonResponse({"response": "403 Forbidden"}, safe=True)

    else:
        return JsonResponse({"response": "405 Method Not Allowed"}, safe=True)


@csrf_exempt       
def suspect_track(request):
    if request.method == "POST":
        try: 
            shape = ast.literal_eval(request.POST.get('shape'))
            buffer = base64.b64decode(request.POST.get('image'))
            # Reconstruct the image
            image = np.frombuffer(buffer, dtype=np.uint8).reshape(shape)
            suspect_id = request.POST.get('suspect_id')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            image_path = f"./media/caught_suspect/{suspect_id}-suspect{random.randint(0,10000000)}.jpg"
            cv2.imwrite(image_path, image)
            # print(type(image))
            

            suspect_instance = suspect_person_detail.objects.get(id=int(suspect_id))
            upload_data = caught_suspect(suspect_id=suspect_instance, latitude=latitude,
                                        longitude=longitude, suspect_image=image_path[1:])
            upload_data.save()

            return JsonResponse({"response": "201 created"}, safe=True)
        except:
            return JsonResponse({"response": "403 Forbidden"}, safe=True)

    else:
        return JsonResponse({"response": "405 Method Not Allowed"}, safe=True)

