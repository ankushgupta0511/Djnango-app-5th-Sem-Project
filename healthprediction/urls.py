from django.contrib import admin
from django.urls import path,include
from healthprediction.views import Symtoms_to_Disease, EyeDiseasePrediction,HeartDiseasePredictionFunction,DiabetesDiseasePredictionFunction
urlpatterns = [

    # path('', Disease_Predictions.as_view(),name='Disease-Predictions'),
    path('eye-disease-prediction/', EyeDiseasePrediction.as_view(),name='eye-disease-prediction'),
    path('symtoms_diagnosis/', Symtoms_to_Disease.as_view(),name='symtoms-to-disease'),

    path('heart_diagnosis/', HeartDiseasePredictionFunction.as_view(),name='heart-disease-prediction'),
    path('diabetes_diagnosis/', DiabetesDiseasePredictionFunction.as_view(),name='diabetes-disease-prediction'),

]
