from django.db import models

# Create your models here.


class Symtoms(models.Model):
    symtoms_name = models.CharField(max_length=400,null=False)
    
    def __str__(self) -> str:
        return f'{self.id} --> {self.symtoms_name}'
    
    


class EyeDiseasePredict(models.Model):
    eye_disease_image = models.ImageField(upload_to="eye_disease_images")
    
    def __str__(self) -> str:
        return f'{self.id}'
    
    

class DiabetesPredict(models.Model):
    Pregnancies	= models.IntegerField()
    Glucose	= models.IntegerField()
    BloodPressure= models.IntegerField()	
    SkinThickness = models.IntegerField()	
    Insulin	= models.IntegerField()
    BMI	= models.IntegerField()
    DiabetesPedigreeFunction = models.IntegerField()
    Age = models.IntegerField()





class HeartDieasesPredict(models.Model):
    age=models.IntegerField()
    sex=models.CharField(max_length=10)
    cp=models.IntegerField()
    trestbps=models.IntegerField()
    chol=models.IntegerField()
    fbs=models.IntegerField()
    restecg=models.IntegerField()
    thalach=models.IntegerField()
    exang=models.IntegerField()
    oldpeak=models.IntegerField()
    slope=models.IntegerField()
    ca=models.IntegerField()
    thal=models.IntegerField()
    
    
