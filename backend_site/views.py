from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.shortcuts import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
import os
import json
import time
import io
# import pickle
import shutil

# import keras.backend.tensorflow_backend as tb
# tb._SYMBOLIC_SCOPE.value = True

# Library for face recognation
import matplotlib.pyplot as plt 
from PIL import Image
from numpy import asarray
import numpy as np
from scipy.spatial.distance import cosine
# from mtcnn.mtcnn import MTCNN
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
import cv2

from .firebase_setting import ref

# Set paths for transfer Images 
Base_dir = os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],'media')
destination = os.path.join(Base_dir, 'suspect_images')

# Loading face detection xml
p = os.path.join(os.path.dirname(os.path.abspath(__file__)),'haarcascade_frontalface_default.xml') 
classifier = cv2.CascadeClassifier(p)

# Initialize vggface model
model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')


"""
Extract face edges
"""
def extract_face_edges(frame, suspect_id, required_size=(224, 224)):
    face = plt.imread(frame)
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = np.asarray(image)
    sample = np.asarray(face_array, 'float32')
    f = preprocess_input(sample, version=2)
    # yhat = []
    # for f in samples:
    face_edges = model.predict(np.expand_dims(f, axis=0))
    # Here firebase data insertion is perform
    face_array_list = np.ndarray.tolist(face_edges)
    face_edges_json = json.dumps(face_array_list)
    ref.push({'id': suspect_id, 'face': face_edges_json})
    # firebase_obj.post('/suspect images', {'id': suspect_id, 'face': face_edges_json})

"""
This function detect face and extract face eadges for face detection
"""
def recognize_face(frame, suspect_id, required_size=(224, 224)):
    pixels = plt.imread(frame)
    # time.sleep(5)
    results = classifier.detectMultiScale(pixels, scaleFactor=1.5, minNeighbors=5)   #two argument added
    samples = []
    for faces in results:
        x1, y1, width, height = faces
        x2, y2 = x1 + width, y1 + height
        # extract the face
        face = pixels[y1:y2, x1:x2]
        # resize pixels to the model size
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = np.asarray(image)
        sample = np.asarray(face_array, 'float32')
        samples.append(preprocess_input(sample, version=2))
    yhat = []
    for f in samples:
        face_edges = model.predict(np.expand_dims(f, axis=0))
        # Here firebase data insertion is perform
        face_array_list = np.ndarray.tolist(face_edges)
        face_edges_json = json.dumps(face_array_list)
        ref.push({
            'id': suspect_id, 
            'face': face_edges_json
        })
        yhat.append(face_edges)

    return yhat


"""
This function load wellcome page of the dashboard
"""
def index(request):
    if request.session.has_key('login_id'):
        data = controller_user.objects.get(id=request.session['login_id'])
        count1 = len(suspect_person_detail.objects.all())
        # print(count1)
        data.name = data.name.split(" ")[0]

        return render(request, 'backend_site/index.html', {'data': data, 'front_count':[count1]})
    else:
        return redirect('login')


"""
This function contain login and section configrations
"""
def login(request):
    if request.session.has_key('login_id'):
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            auth = controller_user.objects.get(email=email, password=password)
            # print(auth.id,"`````````````````````````")
            if auth:
                request.session['login_id'] = auth.id

                return redirect('index')
        except:
            return render(request, 'backend_site/login.html')
    return render(request, 'backend_site/login.html')

def logout(request):
    del request.session['login_id']
    return redirect('login')


"""
This function is use for load add_suspect page
"""
def add_suspect(request):
    if request.session.has_key('login_id'):
        data = controller_user.objects.get(id=request.session['login_id'])
        data.name = data.name.split(" ")[0]
        return render(request, 'backend_site/add_suspect.html', {'data': data})
    else:
        return redirect('login')


"""
This function is for add suspect detail manually
& upload images and that images convert into array and it will be save
"""
def add_suspect_data(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        cnic = request.POST.get('cnic')
        address = request.POST.get('address')
        education = request.POST.get('education')
        marital_status = request.POST.get('marital_status')
        age = request.POST.get('age')
        date_of_birth = request.POST.get('date_of_birth')
        nationality = request.POST.get('nationality')
        description = request.POST.get('description')

        insert_data = suspect_person_detail(first_name=first_name, last_name=last_name,
                                            gender=gender, cnic=cnic, address=address,
                                            education=education, marital_status=marital_status,
                                            age=age, date_of_birth=date_of_birth,
                                            nationalilty=nationality, description=description)

        insert_data.save()

        fs = FileSystemStorage()

        for i in request.FILES:
            request.FILES[i].name = f"{insert_data.id}-suspect.{(request.FILES[i].name).split('.')[-1]}"
            fs.save(request.FILES[i].name, request.FILES[i])

        face_image_array = []
        img_arr_dest = os.path.join(destination,'images_array')

        for img_name in os.listdir(Base_dir):
            if img_name.split('-')[0] == str(insert_data.id):
                shutil.move(os.path.join(Base_dir, img_name), destination)

                # here face dectect and edge extraction is perform
                face_image_array.append(recognize_face(os.path.join(destination,img_name), insert_data.id))
        np.save(os.path.join(img_arr_dest,f"{insert_data.id}_susp_arr.npy"), face_image_array)
        return redirect('add_suspect')

    else:
        return redirect('Add_suspect')


"""
This function is for update suspect data 
"""
def update_suspect(request):
    if request.method == "POST":
        supectId = request.POST.get('suspect_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        cnic = request.POST.get('cnic')
        address = request.POST.get('address')
        education = request.POST.get('education')
        marital_status = request.POST.get('marital_status')
        age = request.POST.get('age')
        # date_of_birth = request.POST.get('date_of_birth')
        nationality = request.POST.get('nationality')
        description = request.POST.get('description')
        status = request.POST.get('status')

        data_table = suspect_person_detail.objects.get(id=supectId)

        data_table.first_name = first_name
        data_table.last_name = last_name
        data_table.gender = gender
        data_table.cnic = cnic
        data_table.address = address
        data_table.education = education
        data_table.marital_status = marital_status
        data_table.age = age
        # data_table.date_of_birth = date_of_birth
        data_table.nationalilty = nationality
        data_table.description = description
        data_table.status = status

        data_table.save()


        return redirect('suspect_list')
    else:
        return redirect('suspect_list')


"""
function for delete suspect profile
"""
def del_suspect(request, suspectId):

    suspect_person_detail.objects.filter(id=suspectId).delete()
    return redirect('suspect_list')



def user(request):
    if request.session.has_key('login_id'):
        data = controller_user.objects.get(id=request.session['login_id'])
        data.name = data.name.split(" ")[0]

        return render(request, 'backend_site/user.html', {'data': data})
    else:
        return redirect('login')


"""
This function is to display all reports
"""
def suspect_list(request):
    if request.session.has_key('login_id'):
        user_data = controller_user.objects.get(id=request.session['login_id'])
        suspect_data = suspect_person_detail.objects.all()
    
        for i in suspect_data:
            # images = [img for img in os.listdir(destination) if img.split('_')[0] =
            i.image = [img for img in os.listdir(destination) if img.split('-')[0] == str(i.id)]
            
        return render(request, 'backend_site/suspects_list.html', {'suspect_data': suspect_data,
                                                                   'data': user_data, 'length':len(suspect_data),
                                                                   'title': 'All Reports', 'sub_title':'Reports'})
    else:
        return redirect('login')


"""
This function is to display suspect that are "Wanted"
"""
def wanted_suspect_list(request):
    if request.session.has_key('login_id'):
        user_data = controller_user.objects.get(id=request.session['login_id'])
        suspect_data = suspect_person_detail.objects.all()
    
        wanted_suspects = []
        for data in suspect_data:
            if data.status == 0:
                wanted_suspects.append(data)


        for i in wanted_suspects:
            # images = [img for img in os.listdir(destination) if img.split('_')[0] =
            i.image = [img for img in os.listdir(destination) if img.split('-')[0] == str(i.id)]
            
        return render(request, 'backend_site/suspects_list.html', {'suspect_data': wanted_suspects,
                                                                   'data': user_data, 'length':len(wanted_suspects),
                                                                   'title': 'Wanted List', 'sub_title':'Wanted List'},)
    else:
        return redirect('login')


"""
This function is to display suspect that case are resolve
"""
def case_reslove_list(request):
    if request.session.has_key('login_id'):
        user_data = controller_user.objects.get(id=request.session['login_id'])
        suspect_data = suspect_person_detail.objects.all()
    
        resolve_suspects = []
        for data in suspect_data:
            if data.status == 2:
                resolve_suspects.append(data)


        for i in resolve_suspects:
            # images = [img for img in os.listdir(destination) if img.split('_')[0] =
            i.image = [img for img in os.listdir(destination) if img.split('-')[0] == str(i.id)]
            
        return render(request, 'backend_site/suspects_list.html', {'suspect_data': resolve_suspects,
                                                                   'data': user_data, 'length':len(resolve_suspects),
                                                                   'title': 'Resolve Cases', 'sub_title':'Resolve Case'},)
    else:
        return redirect('login')


"""
This function is to display suspect that are "Found"
"""
def suspect_found_list(request):
    if request.session.has_key('login_id'):
        user_data = controller_user.objects.get(id=request.session['login_id'])
        suspect_data = suspect_person_detail.objects.all()
    
        resolve_suspects = []
        for data in suspect_data:
            if data.status == 1:
                resolve_suspects.append(data)


        for i in resolve_suspects:
            # images = [img for img in os.listdir(destination) if img.split('_')[0] =
            i.image = [img for img in os.listdir(destination) if img.split('-')[0] == str(i.id)]
            
        return render(request, 'backend_site/suspects_list.html', {'suspect_data': resolve_suspects,
                                                                   'data': user_data, 'length':len(resolve_suspects),
                                                                   'title': 'Suspect Found', 'sub_title':'Found suspects'},)
    else:
        return redirect('login')


"""

"""
def identify_suspects(request):
    if request.session.has_key('login_id'):
        data = controller_user.objects.get(id=request.session['login_id'])
        identify_suspect = suspect_person_detail.objects.get(status=True)
        # print(identify_suspect,'``````````````')
        try:
            return render(request, 'backend_site/suspects_list.html', {'identify_suspect': identify_suspect,
                                                                       'data': data, 'length':len(identify_suspect)})
        except:
            # print(identify_suspect.first_name)
            return render(request, 'backend_site/identify_suspects.html', {'identify_suspect': identify_suspect,
                                                                       'data': data, 'length': 0})
    else:
        return redirect('login')


"""
list for uploading video from resgister user
"""
def appUser_registered(request):
    if request.session.has_key('login_id'):
        data = controller_user.objects.get(id=request.session['login_id'])
        suspects_data = suspect_from_app_User.objects.all()
        all_suspect = []
        for suspect in suspects_data: 
            if suspect.status == 0:
                all_suspect.append(suspect)
        
        try:
            return render(request, 'backend_site/suspects_from_user.html', {'all_suspect': all_suspect,
                                                                            'data': data, 'length':len(all_suspect),
                                                                            'title': 'Suspect from Registered user', 'sub_title':'AppUser Suspect'})
        except:
            # print(identify_suspect.first_name)
            return render(request, 'backend_site/index.html', {'data': data, 'length': 0,
                                                               'r_sus': regist_sus, 'a_sus': anon_sus, 'all_sus': all_sus})
    else:
        return redirect('login')


"""
list for uploading video from anonymous user
"""
def appUser_anonymous(request):
    if request.session.has_key('login_id'):
        data = controller_user.objects.get(id=request.session['login_id'])
        suspects_data = suspect_from_anonymous.objects.all()
        all_suspect = []
        for suspect in suspects_data: 
            if suspect.status == 0:
                all_suspect.append(suspect)

        try:
            return render(request, 'backend_site/suspect_from_anonymous.html', {'all_suspect': all_suspect,
                                                                            'data': data, 'length':len(all_suspect),
                                                                            'title': 'Suspect from Anonymous user', 'sub_title':'AppUser Suspect'})
        except:
            # print(identify_suspect.first_name)
            return render(request, 'backend_site/index.html', {'data': data, 'length': 0,
                                                                'r_sus': regist_sus, 'a_sus': anon_sus, 'all_sus': all_sus})
    else:
        return redirect('login')


"""
Delete use complain
"""
def delete_user_complain(request): 
    selector = request.GET.get('selector')
    complain_id = request.GET.get('id')

    if selector == '0':
        video_url = suspect_from_app_User.objects.get(id=complain_id)
    else:
        video_url = suspect_from_anonymous.objects.get(id=complain_id)

    video_imgs_urlName = video_url.video_url.split("/")[2].split(".")[0]
    images_dir = os.path.join(Base_dir, 'video_images')
    video_imgs_dir = os.path.join(images_dir, video_imgs_urlName)

    # print(os.listdir(images_dir).count(video_imgs_urlName))
    if os.listdir(images_dir).count(video_imgs_urlName) > 0:
        shutil.rmtree(video_imgs_dir)
    
    video_url.delete()
    return JsonResponse({'msg': 'Successfully Deleted!'})


"""
This function is call by 'scan_video' function to process video
"""
def process_video(url, imgs_dir):
    c = 0
    cap = cv2.VideoCapture(f".{url}") 
    while (cap.isOpened()): 
        ret, frame = cap.read()
        if( ret != True):
            break
        
        faces = classifier.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)   
        if len(faces) != 0:
            for (x, y, w, h) in faces:
                c += 1
                img_path = os.path.join(imgs_dir, f"suspect{c}.jpg")
                cv2.imwrite(img_path, frame[y:y+h, x:x+w])
              

"""
This function is call by ajax from frontend javascript code.
It scan video and extract all the face from it and display on frontend.
"""
def scan_video(request):
    video_url = request.GET.get('url')
    video_imgs_urlName = video_url.split("/")[2].split(".")[0]
    images_dir = os.path.join(Base_dir, 'video_images')

    video_imgs_dir = os.path.join(images_dir, video_imgs_urlName)

    if os.listdir(images_dir).count(video_imgs_urlName) < 1:
        os.mkdir(video_imgs_dir)
    
        process_video(video_url, video_imgs_dir)

    all_images = os.listdir(video_imgs_dir)

    return JsonResponse({'images': all_images, 'path': video_imgs_urlName})


"""
This function add suspect into wanted list
"""
def add_suspect_from_video(request):
    imgs_arr = request.GET.get('imgs_arr')
    attr_id = request.GET.get('attr_id')
    selector = request.GET.get('selector')

    if selector == '0':
        video_obj = suspect_from_app_User.objects.get(id=attr_id)
    else:
        video_obj = suspect_from_anonymous.objects.get(id=attr_id)
 
    video_imgs_urlName = video_obj.video_url.split("/")[-1].split('.')[0]
    images = json.loads(imgs_arr)['imgs']

    images_dir = os.path.join(Base_dir, 'video_images')
    video_imgs_dir = os.path.join(images_dir, video_imgs_urlName)

    suspect_img_dir = os.path.join(Base_dir, 'suspect_images')
    data = suspect_person_detail()
    data.save()

    for i, v in enumerate(images):
        os.rename(os.path.join(video_imgs_dir, v), os.path.join(video_imgs_dir, f"{data.id}-suspect{i}.jpg"))
        shutil.copyfile(os.path.join(video_imgs_dir, f"{data.id}-suspect{i}.jpg"), os.path.join(suspect_img_dir, f"{data.id}-suspect{i}.jpg"))
        extract_face_edges(os.path.join(video_imgs_dir, f"{data.id}-suspect{i}.jpg"), data.id)
    
    if os.listdir(images_dir).count(video_imgs_urlName) > 0:
        shutil.rmtree(video_imgs_dir)

    video_obj.delete()

    return JsonResponse({'msg': "Successfully saved!"})


"""
This function is to display suspect that are track
"""
def track_suspects(request):
    if request.session.has_key('login_id'):
        user_data = controller_user.objects.get(id=request.session['login_id'])
        suspect_data = suspect_track_list.objects.all()

        return render(request, 'backend_site/track_suspect_list.html', {'suspect_data': suspect_data,
                                                                   'data': user_data, 'length':len(suspect_data),
                                                                   'title': 'Tracked Suspect', 'sub_title':'Tracked Suspect'},)
    else:
        return redirect('login')


"""
Function for Ajax to get all images url for track suspect
"""
def get_track_suspect_images(request):
    id = request.GET.get('id')

    suspect_data = caught_suspect.objects.filter(suspect_id=suspect_track_list.objects.get(id=id))
    urls = []
    date_time = []
    for items in suspect_data:
        urls.append(items.suspect_image)
        date_time.append(items.report_date_time)

    return JsonResponse({'urls': urls, 'dataTime': date_time})


"""
Function for Ajax to get all latitude and longitude for track suspect
"""
def get_track_location(request):
    id = request.GET.get('id')
    suspect_id = request.GET.get('suspect_id')
    update_status = suspect_track_list.objects.filter(suspect_id=int(suspect_id))[0]
    update_status.status = 1
    update_status.save()
    # print(update_status)
    suspect_data = caught_suspect.objects.filter(suspect_id=suspect_track_list.objects.get(id=id))
    location = []
    for items in suspect_data:
        location.append({'lat': items.latitude, 'lng': items.longitude})
    
    return JsonResponse({'cords': location})


"""
get notification
"""
def get_notification(request):
    register_complain = len(suspect_from_app_User.objects.all())
    anonymous_complain = len(suspect_from_anonymous.objects.all())
    track_suspects = suspect_track_list.objects.all()
    total_catch_suspect = len(caught_suspect.objects.filter(status = 1))
    t_s = []
    for suspect in track_suspects:
        if suspect.status == 1:
            t_s.append(suspect)

    track_suspect = caught_suspect.objects.filter(status = 0)
    catch_suspect = len(track_suspect)
    for data in track_suspect:
        data.status = 1
        data.save()

    return JsonResponse({'tc_s': total_catch_suspect, 'track_status': catch_suspect, 'r_c': register_complain, 'a_c': anonymous_complain, 't_s': len(t_s), 't_s_r': len(suspect_person_detail.objects.all())})


"""
list of suspect that track recently
"""
def recent_track_suspect(request):
    if request.session.has_key('login_id'):
        user_data = controller_user.objects.get(id=request.session['login_id'])
        track_suspect = caught_suspect.objects.filter(status = 1)

        return render(request, 'backend_site/recent_track_suspect.html', {'suspect_data': track_suspect,
                                                                       'data': user_data, 'length':len(track_suspect),
                                                                       'title': 'Tracked Suspect', 'sub_title':'Tracked Suspect'},)
    else:
        return redirect('login')


"""
change suspect status to 2
"""
def change_suspect_status(request):
    update_status = caught_suspect.objects.get(id=int(request.GET.get('suspect_id')))  
    update_status.status = 2
    update_status.save()

    return JsonResponse({'res': 'Done!'})