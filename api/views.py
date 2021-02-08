from django.shortcuts import render, redirect
from .models import *
from backend_site.models import suspect_from_app_User, app_user, suspect_from_anonymous, caught_suspect, suspect_track_list
from .serializers import serializer_suspectData
from django.http import HttpResponse, JsonResponse
import sys
import ast
import base64
import numpy as np
import cv2
import random
import datetime
from django.utils import timezone
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


# @csrf_exempt
# def creat_app_user(request):
#     if request.method == "POST":
#         # try: 
#         # stream = io.BytesIO(request.body)
#         # python_data = JSONParser().parse(stream)
#         print(request.POST)
#         return JsonResponse({"response": "201 created"}, safe=True)
#         # except:
#         #     return JsonResponse({"response": "403 Forbidden"}, safe=True)

#     else:
#         return JsonResponse({"response": "405 Method Not Allowed"}, safe=True)


@csrf_exempt       
def suspect_track(request):
    if request.method == "POST":
        # try: 
        shape = ast.literal_eval(request.POST.get('shape'))
        buffer = base64.b64decode(request.POST.get('image'))
        # Reconstruct the image
        image = np.frombuffer(buffer, dtype=np.uint8).reshape(shape)
        suspect_id = request.POST.get('suspect_id')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        image_path = f"./media/caught_suspect/{suspect_id}-suspect{random.randint(0,10000000)}.jpg"
        cv2.imwrite(image_path, image)
        suspect_instance = suspect_person_detail.objects.get(id=suspect_id)

        if len(suspect_track_list.objects.filter(suspect_id=suspect_instance)) == 0:
            tracked_suspect = suspect_track_list(suspect_id=suspect_instance)
            tracked_suspect.save()
        else:
            tracked_suspect = suspect_track_list.objects.filter(suspect_id=suspect_instance)[0]
            tracked_suspect.recent_track_date_time = timezone.now()
            tracked_suspect.status = 0
            tracked_suspect.save()

        upload_data = caught_suspect(suspect_id=tracked_suspect, latitude=latitude,
                                    longitude=longitude, suspect_image=image_path[1:])
        upload_data.save()

        return JsonResponse({"response": "201 created"}, safe=True)
        # except:
        #     return JsonResponse({"response": "403 Forbidden"}, safe=True)

    else:
        return JsonResponse({"response": "405 Method Not Allowed"}, safe=True)



@csrf_exempt 
def check_username_email(request):
    if request.method == "POST":
        try: 
            login_status = 2
            cnic = request.POST['cnic']
            email = request.POST['email']
            username = request.POST['username']

            # print(cnic, email, username)
            check_cnic = len(app_user.objects.filter(cnic=cnic))
            check_email = len(app_user.objects.filter(email=email))
            check_username = len(app_user.objects.filter(full_name=username))

            if check_cnic == 0 and check_email == 0 and check_username == 0:
                login_status = 0
            else: 
                login_status = 1

            print(login_status)


            return JsonResponse({"status": login_status, "credStatus": [check_username, check_cnic, check_email]}, safe=True)
        except:
            return JsonResponse({"response": "403 Forbidden"}, safe=True)

    else:
        return JsonResponse({"response": "405 Method Not Allowed"}, safe=True)


@csrf_exempt 
def creat_app_user(request):
    if request.method == "POST":
        try: 
            cnic = request.POST['cnic']
            email = request.POST['email']
            number = request.POST['number']
            password = request.POST['password']
            full_name = request.POST['full_name']
            gender = request.POST['gender']
            DOB = request.POST['DOB']
            city = request.POST['city']
            # print(cnic,' ',email,' ',number,' ',password,' ',full_name,' ',' ',gender,' ',city,' ',DOB)
            
            new_user = app_user(full_name=full_name, 
                                email=email, password=password, 
                                gender=gender, cnic=cnic,
                                city=city, date_of_birth=DOB,
                                phone_number=number)
            
            new_user.save()
            return JsonResponse({"resp": 0}, safe=True)
        except:
            return JsonResponse({"resp": 1}, safe=True)

    else:
        return JsonResponse({"response": "405 Method Not Allowed"}, safe=True)