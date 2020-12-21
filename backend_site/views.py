from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.shortcuts import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import json
import time

# import pickle
import shutil

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

from .firebase_setting import firebase_obj

# Set paths for transfer Images 
Base_dir = os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],'media')
destination = os.path.join(Base_dir, 'suspect_images')

# Loading face detection xml
p = os.path.join(os.path.dirname(os.path.abspath(__file__)),'haarcascade_frontalface_default.xml') 
classifier = cv2.CascadeClassifier(p)

# Initialize vggface model
model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')


"""
This function extract face eadges for face detection
"""
def recognize_face(frame, suspect_id, required_size=(224, 224)):
    pixels = plt.imread(frame)
    time.sleep(5)
    results = classifier.detectMultiScale(pixels)  
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
        firebase_obj.post('/suspect images', {'id': suspect_id, 'face': face_edges_json})
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

        regist_sus = len(suspect_from_app_User.objects.all())
        anon_sus = len(suspect_from_anonymous.objects.all())
        all_sus = regist_sus + anon_sus

        return render(request, 'backend_site/index.html', {'data': data, 'front_count':[count1],
                                                            'r_sus': regist_sus, 'a_sus': anon_sus, 'all_sus': all_sus})
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

        regist_sus = len(suspect_from_app_User.objects.all())
        anon_sus = len(suspect_from_anonymous.objects.all())
        all_sus = regist_sus + anon_sus

        return render(request, 'backend_site/user.html', {'data': data,
                                                          'r_sus': regist_sus, 'a_sus': anon_sus, 'all_sus': all_sus})
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

        regist_sus = len(suspect_from_app_User.objects.all())
        anon_sus = len(suspect_from_anonymous.objects.all())
        all_sus = regist_sus + anon_sus
            
        return render(request, 'backend_site/suspects_list.html', {'suspect_data': suspect_data,
                                                                   'data': user_data, 'length':len(suspect_data),
                                                                   'title': 'All Reports', 'sub_title':'Reports',
                                                                   'r_sus': regist_sus, 'a_sus': anon_sus, 'all_sus': all_sus})
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
        
        regist_sus = len(suspect_from_app_User.objects.all())
        anon_sus = len(suspect_from_anonymous.objects.all())
        all_sus = regist_sus + anon_sus
        try:
            return render(request, 'backend_site/suspects_from_user.html', {'all_suspect': all_suspect,
                                                                            'data': data, 'length':len(all_suspect),
                                                                            'title': 'Suspect from Registered user', 'sub_title':'AppUser Suspect',
                                                                            'r_sus': regist_sus, 'a_sus': anon_sus, 'all_sus': all_sus})
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

        regist_sus = len(suspect_from_app_User.objects.all())
        anon_sus = len(suspect_from_anonymous.objects.all())
        all_sus = regist_sus + anon_sus

        # print(regist_sus,'===',anon_sus,'===',all_sus)

        try:
            return render(request, 'backend_site/suspect_from_anonymous.html', {'all_suspect': all_suspect,
                                                                            'data': data, 'length':len(all_suspect),
                                                                            'title': 'Suspect from Anonymous user', 'sub_title':'AppUser Suspect',
                                                                            'r_sus': regist_sus, 'a_sus': anon_sus, 'all_sus': all_sus})
        except:
            # print(identify_suspect.first_name)
            return render(request, 'backend_site/index.html', {'data': data, 'length': 0,
                                                                'r_sus': regist_sus, 'a_sus': anon_sus, 'all_sus': all_sus})
    else:
        return redirect('login')