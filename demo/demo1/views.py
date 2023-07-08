from django.shortcuts import render,redirect
from django.conf import settings
from .forms import RegisterForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import os

import tensorflow as tf
# import keras
from keras.models import load_model
from tensorflow import Graph,Session
# from keras.preprocessing import image
# import json
# from tensorflow.keras.layers import conv2D,Dense,Input,Conv2DTranspose,AveragePooling2D,UpSampling2D
# from tensorflow.keras.models import Model
# from tensorflow.keras.datasets import cifar100
# from tensorflow.keras.callbacks import EarlyStopping
# from PIL import Image
# import numpy as np
# import pandas as pd





# model=load_model('./models/')
model_graph=Graph()
with model_graph.as_default():
    tf_session=Session()
    with tf_session.as_default():
        model=load_model('./models/model.joblib')





# Create your views here.
@login_required
def index(request):
    # Handle form submission
    if request.method == 'POST' and request.FILES['image']:
        # Get the uploaded image file
        image_file = request.FILES['image']
        # Save the image file to the server
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        result = fs.url(filename)
        # uploaded_file_url = fs.url(filename)
        # Remove the uploaded image file from the server
        # os.remove(os.path.join(settings.MEDIA_ROOT, filename))
        #Code for image processing

        with model_graph.as_default():
            with tf_session.as_default():
                predi=model.predict(result)


        context = {'result':result}
        # context = {'result':predi}
        # Render the result page with the restored image
        # context = {'result': fs.url(restored_img_filename)}
        # return render(request, 'index.html', context)
        return render(request, 'demo/index.html',context)
    # Render the index page with the upload form
    context = {}
    return render(request, 'demo/index.html', context)

def register(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        print(form.error_messages)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request,'demo/register.html',{'form':form})