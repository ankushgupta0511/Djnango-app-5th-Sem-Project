from django.shortcuts import render
from healthprediction.serializers import Symtoms_to_DiseaseSerializer,EyeDiseasePredictionSerializer,ChatGPTSerializer,DiabetesDiseasePredictionFunctionSerializer,HeartDiseasePredictionFunctionSerializer
import json

# 

import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt




from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import EyeDiseasePredictionSerializer


from tensorflow.keras.models import load_model
model = load_model('model/Eye_Disease_DL_Model.h5')



# 
import openai 


from rest_framework.parsers import MultiPartParser, FormParser

import os


from healthprediction.seed import get_predicted_value,helper

import pickle
svc = pickle.load(open('model/svc.pkl','rb'))



# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate # import here authenticate
from account.renderers import UserRenderer   # import custome errors

from rest_framework.permissions import IsAuthenticated




class Symtoms_to_Disease(APIView):
    renderer_classes = [UserRenderer]   # ab all 'error' word show before error text
    def post(self, request,format=None):
        
        
        serializer = Symtoms_to_DiseaseSerializer(data=request.data)
        
        
        
        model = svc.predict([[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

        # svc.predict(X_test.iloc[100].values.reshape(1,-1))
        print('\n\n')
        print('testing 1')
        print('prediction :- ',model[0])
        print('\n\n')
        
       
    
        if serializer.is_valid(raise_exception=True):
            print('testing 2 :- ',serializer.data)
            symtoms_name = serializer.data.get('symtoms_name')
            print('symtoms_name is :- ',symtoms_name)
            # print('symtoms_name type is :- ',type(symtoms_name))
            
            # symptoms = 'itching,skin_rash,nodal_skin_eruptions'
            # symptoms = ' skin_rash, high_fever, blister, red_sore_around_nose'
            # symptoms = ' skin_rash,  joint_pain,  skin_peeling,  silver_like_dusting'
            
            try:
                
                symptoms = f"{symtoms_name}"
                user_symptoms = [s.strip() for s in symptoms.split(',')]
                user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
                predicted_disease = get_predicted_value(user_symptoms)
                print('\n','predicted_disease testing :- ',predicted_disease,'\n')
                desc, pre, med, die, wrkout = helper(predicted_disease)
                
                
                print("=================precautions==================")
                pre = ', '.join(pre[0])
                print(pre)



                print("=================medications==================")
                import ast
                string_list = med
                actual_list = ast.literal_eval(string_list[0])
                medi = ', '.join(actual_list)
                print(medi)
                
                
                
                
                
                print("=================workout==================")
                workout = (', '.join(wrkout))
                print(workout)
                
                

                            
                print("=================diets==================")
                import ast
                string_list = die
                actual_list = ast.literal_eval(string_list[0])
                diets = ', '.join(actual_list)
                print(diets)
                            
                            
            
                data = {
                    "symtoms_name":symtoms_name,
                    "predicted_disease":predicted_disease,
                    "predicted_descriptions":desc,
                    "predicted_precations":pre,   
                    "predicted_medications":medi,
                    "predicted_diets":diets,
                    "predicted_workout":workout,
                    "msg":"Successfully Model Predictions!!"
                }
            except Exception as e:
                print("\n\n Logical Error   \n\n")
                # return Response({'Predictions_error':"somethings wrong!!"},status=status.HTTP_201_CREATED)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                
             
            return Response({'Predictions':data},status=status.HTTP_201_CREATED)
        
        print('error testing')
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    







class EyeDiseasePrediction(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Allow file uploads
    renderer_classes = [UserRenderer]   # ab all 'error' word show before error text


    def post(self, request, *args, **kwargs):
        print('Request data:', request.data)
        print('Request FILES:', request.FILES)

        serializer = EyeDiseasePredictionSerializer(data=request.data)
        print("testing 1")
        if serializer.is_valid():
            print("testing 1")
            eye_disease_image = request.FILES.get('eye_disease_image')
            print('Uploaded file:', eye_disease_image)
            try:
                # Convert the image file to an OpenCV-compatible format
                image = Image.open(eye_disease_image)  # Open the image using PIL
                open_cv_image = np.array(image)  # Convert the PIL image to a NumPy array
                print("open_cv_image :- ",open_cv_image)
                print("open_cv_image.shape :- ",open_cv_image.shape)
                print("open_cv_image.shape[-1] :- ",open_cv_image.shape[-1])

                # If the image is RGBA (has an alpha channel), convert it to RGB
                if open_cv_image.shape[-1] == 4:
                    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGBA2RGB)
                    print("open_cv_image :- ",open_cv_image)
                
                # Now, `open_cv_image` can be processed by OpenCV
                print('Image shape:', open_cv_image.shape)
                # plt.imshow(open_cv_image)  # Display the image (Optional for debugging)
                # plt.show()  # This will show the image in the console if you have a GUI

                # Save the image to the model (after OpenCV processing if needed)
                # serializer.save()  # Save the uploaded file
                
                
                
                open_cv_image = cv2.resize(open_cv_image,(256,256))
                print('open_cv_image.shape :', open_cv_image.shape)
                test_input = open_cv_image.reshape((1,256,256,3))
                eye_output = model.predict(test_input)
                print("\n\n\neye_output\n\n\n",eye_output)
                
                #  ["cataract", "diabetic_retinopathy", "glaucoma", "normal"]
                
                disease_array = [ int(i) for i in eye_output[0]]
                print(disease_array)

                disease = ""
                
                if disease_array[0] == 1:
                    disease = "cataract"
                elif disease_array[1] == 1:
                    disease = "diabetic_retinopathy"
                elif disease_array[2] == 1:
                    disease = "glaucoma"
                else:
                    disease = "normal"
                
                print(disease) 
                
                prediction = {
                    "disease":disease,
                    "msg": "Image successfully uploaded and processed!!"
                } 
                
                return Response({'Prediction': prediction}, status=status.HTTP_200_OK)
            except Exception as e:
                print('Error processing image:', e)
                return Response({'error': 'Error processing the image'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        










# class ChatGPTDiseaseQuery(APIView):
#     renderer_classes = [UserRenderer]   # ab all 'error' word show before error text
#     def post(self, request,format=None):
#         print("testing 1")
#         serializer = ChatGPTSerializer(data=request.data)
#         print("testing 2")
#         if serializer.is_valid(raise_exception=True):
#             print("testing 3")
#             Disease_query = serializer.data.get('query')
#             print("testing 4")
#             user_input = Disease_query  # Get input from the user

#             # Call OpenAI API
#             openai.api_key = os.environ.get('OPENAI_API_KEY')
            
#             print('chatgpt API :- ',os.environ.get('OPENAI_API_KEY'))
            
            
#             try:
                
#                 # response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[...])

#                 response = openai.ChatCompletion.create(
#                     model="gpt-3.5-turbo",
#                     messages=[
#                         # {"role": "system", "content": "You are a helpful assistant."},
#                         {"role": "user", "content": user_input},
#                     ]
#                 )

#                 # Extract the model's response
#                 gpt_response = response['choices'][0]['message']['content']
#                 print("Completed response of Chatgpt API!!")
#                 print(f"\n\n {gpt_response} \n\n")
#                 return Response({'Predicted_response': gpt_response},status=status.HTTP_201_CREATED)
#                 # return JsonResponse({'response': gpt_response})

#             except Exception as e:
#                 print("UnCompleted response of Chatgpt API!!")
#                 return Response({'error': str(e)},status=status.HTTP_400_BAD_REQUEST)
#                 # return JsonResponse({'error': str(e)})
            
            
            
            
#             # return Response(status=status.HTTP_400_BAD_REQUEST)
        

#         else:
#             print('error testing')
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
class DiabetesDiseasePredictionFunction(APIView):
    renderer_classes = [UserRenderer]   # ab all 'error' word show before error text
    def post(self, request,format=None):
        print("testing 1")
        serializer = DiabetesDiseasePredictionFunctionSerializer(data=request.data)
        print("testing 2")
        if serializer.is_valid(raise_exception=True):
            print("testing 3")
            # serializer.save()
                
            Pregnancies = serializer.data.get('Pregnancies')
            Glucose = serializer.data.get('Glucose')
            BloodPressure = serializer.data.get('BloodPressure')
            SkinThickness = serializer.data.get('SkinThickness')
            Insulin = serializer.data.get('Insulin')
            BMI = serializer.data.get('BMI')
            DiabetesPedigreeFunction = serializer.data.get('DiabetesPedigreeFunction')
            Age = serializer.data.get('Age')
            
            
            print("Pregnancies : ",Pregnancies)
            print("Glucose : ",Glucose)
            print("BloodPressure : ",BloodPressure)
            print("SkinThickness : ",SkinThickness)
            print("Insulin : ",Insulin)
            print("BMI : ",BMI)
            print("DiabetesPedigreeFunction : ",DiabetesPedigreeFunction)
            print("Age : ",Age)
            

            





            prediction = {
                    "msg": "Successfully Diabetes predict!!",
                    "disease":" rajvarthan diabtise "
                } 
            return Response({'Prediction': prediction},status=status.HTTP_201_CREATED)
            
        else:
            print('error testing')
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


        
class HeartDiseasePredictionFunction(APIView):
    renderer_classes = [UserRenderer]   # ab all 'error' word show before error text
    def post(self, request,format=None):
        print("testing 1")
        serializer = HeartDiseasePredictionFunctionSerializer(data=request.data)
        print("testing 2")
        if serializer.is_valid(raise_exception=True):
            print("testing 3")
            serializer.save()
            

            age = serializer.data.get('age')
            sex = serializer.data.get('sex')
            cp = serializer.data.get('cp')
            trestbps = serializer.data.get('trestbps')
            chol = serializer.data.get('chol')
            fbs = serializer.data.get('fbs')
            restecg = serializer.data.get('restecg')
            thalach = serializer.data.get('thalach')
            exang = serializer.data.get('exang')
            oldpeak = serializer.data.get('oldpeak')
            slope = serializer.data.get('slope')
            ca = serializer.data.get('ca')
            thal = serializer.data.get('thal')
            
            
            
            print("age : ",age)
            print("sex : ",sex)
            print("cp : ",cp)
            print("trestbps : ",trestbps)
            print("chol : ",chol)
            print("fbs : ",fbs)
            print("Glucose : ",restecg)
            print("BloodPressure : ",thalach)
            print("SkinThickness : ",exang)
            print("Insulin : ",oldpeak)
            print("BMI : ",slope)
            print("DiabetesPedigreeFunction : ",ca)
            print("Age : ",thal)
            
            
            
            prediction = {
                    "msg": "Successfully Diabetes predict!!",
                    "disease":"Nidhi heart disease"
                } 



            return Response({'Prediction': prediction},status=status.HTTP_201_CREATED)
            
        
        else:
            print('error testing')
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            