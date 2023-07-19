from django.shortcuts import render
from .forms import ImageForm
from .model_loader import load_model
#from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.applications.inception_v3 import preprocess_input

from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            image_path = image_instance.image.path
            print(image_path)
            # Execute the script with the image path using subprocess
            # command = ['python', 'path/to/script.py', '--img_path', image_path]
            # output = subprocess.check_output(command, universal_newlines=True)
            # print(output)
            return render(request, 'detection_page/home_detection.html', {'form': form})
    else:
        form = ImageForm()
    return render(request, 'detection_page/home_detection.html', {'form': form})

import time
from django.http import JsonResponse
from django.shortcuts import render
from .forms import ImageForm


from django.conf import settings
import os


from django.shortcuts import render, redirect

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import ImageForm
from django.conf import settings
import os

def classify_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            model = load_model()

            # Process and classify the image using the loaded model
            img = Image.open(image)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            #img_array = np.array(img.resize((299, 299)))
            target_size = (299, 299)  # Adjust to the desired target size
            img = img.resize(target_size)
           

            img_array = np.array(img)
            preprocessed_img = preprocess_input(img_array)
            print(img_array.shape)
            # Expand dimensions if necessary
            preprocessed_img = np.expand_dims(preprocessed_img, axis=0)

            # Measure prediction time
            start_time = time.time()

            # Perform the prediction
            result = model.predict(preprocessed_img)
            predicted_class = np.argmax(result, axis=1)
            predicted_probability = np.max(result)
           

            # Calculate prediction time
            end_time = time.time()
            prediction_time = end_time - start_time

            # Return the classification result, probabilities, and prediction time to the template
            classes = ['Cyclone', 'Drought', 'Earthquake', 'Flood', 'Landslide', 'Non_Damage_Buildings_Streets',
                       'Non_Damage_WildFire_Forest', 'Sea', 'Urban_Fire', 'Wild_Fire']
            predicted_label = classes[int(predicted_class)]
            probabilities = result.flatten().tolist()

            # Save the uploaded image to a location accessible by the template
            image_name = image.name
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            if predicted_probability < 0.7:
                result_message = "The image cannot be classified as any disaster type and of the non damage classes present in the dataset."
                predicted_label = ""
            else:
                result_message = predicted_label
            # Save the results to Excel
            save_results_to_excel(image_name, predicted_label, probabilities, prediction_time)

            context = {
                'result': result_message,
                'prediction_time': prediction_time,
                'image_url': settings.MEDIA_URL + image_name,
                'probabilities': probabilities,
                'predicted_label': predicted_label
            }

            return render(request, 'detection_page/index.html', context)
        else:
            return redirect('classify_image')  # Redirect to the home_detection page if no image is uploaded
    else:
        form = ImageForm()
        return render(request, 'detection_page/home_detection.html', {'form': form})



def back_button(request):
    if request.method == 'POST':
        form = ImageForm()
        return redirect('classify_image')
    

import pandas as pd
def save_results_to_excel(image_name, predicted_label, probabilities, prediction_time):
    data = {'Image Name': [image_name],
            'Predicted Label': [predicted_label],
            'Probabilities': [probabilities],
            'Prediction Time': [prediction_time]}
    
    df = pd.DataFrame(data)
    
    # Specify the desired Excel file path
    excel_file_path = 'C:/Users/Anisha/DjangoUI/DisasterDetection/ExcelSheet/classification_results.xlsx'
    df.to_excel(excel_file_path, index=False, header=True)