from django.contrib import admin

# Register your models here.

from healthprediction.models import Symtoms,ChatGPTQuery
from .models import EyeDiseasePredict,DiabetesPredict

admin.site.register(Symtoms)
admin.site.register(ChatGPTQuery)
admin.site.register(EyeDiseasePredict)
admin.site.register(DiabetesPredict)