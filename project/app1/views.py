#views.py
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import os
import cv2
import numpy as np
import keras
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import tensorflow_addons as tfa
import tensorflow as tf
model = tf.keras.models.load_model('./app1/BT_CNN_model7.h5', custom_objects={'F1Score': tfa.metrics.F1Score})
ci=['Bengin cases','Malignant cases','Normal cases']
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import MRIImage  # Import the model for MRIImage
@login_required(login_url='login')

def HomePage(request):
    if request.method == 'POST':
        # Check if the form is valid (i.e., an image is uploaded)
        if 'image' in request.FILES:
            uploaded_image = request.FILES['image']
            # username = request.user.username
            # mri_image = MRIImage.objects.create(image=uploaded_image, username=username)
            # request.session['username'] = username

            # Perform image prediction
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)

            # Save the file to disk
            filename = fs.save(uploaded_image.name, uploaded_image)

            # Get the file path
            image_path = fs.path(filename)
            
            image = cv2.imread(image_path)
            image = cv2.resize(image, (256, 256))
            image = image / 255.0
            image = np.expand_dims(image, axis=0)
            
            prediction = model.predict(image)
            predicted_class_index = np.argmax(prediction[0])
            predicted_class = ci[predicted_class_index]
            if predicted_class != None:
                return render(request, 'home.html', {'predicted_class': predicted_class})


    return render(request,'home.html')


def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')