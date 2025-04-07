# Djnango-app-5th-Sem-Project


before starting add model folder and .env file into root directory!! you can get this model folder into google drive 
 https://drive.google.com/drive/folders/1q9wD-278mEhFobt1uptn09wjsCrtoVbS?usp=sharing




# important command it remove all problem of power shell
```
// Run following command in Windows Powershell ISE  in our system
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```



# this command imp which install freeze and give all dependencies in txt file
```
python -m pip freeze > requirements.txt
```



# install all dependencies which written in requirements.txt file
```
pip install -r requirements.txt
```

# error arise and verry bad error
```
Fatal error in launcher: Unable to create process using '"E:\All_programe_new_folder\Django With React  by Geeky Shows\Full Authentication Using Django With React\env\Scripts\python.exe"  "E:\All_programe_new_folder\ankushgupta 5th sem\Minor Project 5th Sem\DjangoWithReact Minor Project Temp\env\Scripts\pip.exe" --version': The system cannot find the file specified.


// resolve it help by fire command cmd


```



# install packages inside 'djangoauthapi1'
``` 
pip install djangorestframework



// simple jwt packages :- https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html
pip install djangorestframework-simplejwt





// setting.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
    ...
]



from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),



    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",


    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}











// import i urls.py  it provide access token for login 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ...
]

``` 




# course policy error
```
// https://pypi.org/project/django-cors-headers/
pip install django-cors-headers


// import in setting.py
INSTALLED_APPS = [
    ...,
    "corsheaders",
    ...,
]


// import in setting.py
MIDDLEWARE = [
    ...,
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...,
]




// import in setting.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3080",
    "http://127.0.0.1:3000",
]

```


# full example of customizing authentication 
```
// https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#a-full-example


```



# Note :- Errors Detail Show like this in terminal
```
    {'email': [ErrorDetail(string='This field is required.', code='required')], 'name': [ErrorDetail(string='This field is required.', code='required')], 'password': [ErrorDetail(string='This field is required.', code='required')], 'password2': [ErrorDetail(string='This field is required.', code='required')], 'tc': [ErrorDetail(string='This field is required.', code='required')]}
```




# Creating tokens manually
```
// source :-  https://django-rest-framework-simplejwt.readthedocs.io/en/latest/creating_tokens_manually.html


from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

```





# Note :- for getting current user profile then you basic need a token and then maro request in postman like [ Bearer <Toekn> ]  then jo user login honga wo aapko mil jayenga as a output

```
// for example 

// maro request on url :- http://127.0.0.1:8000/api/user/profile/

// write code in HTTP headers in postman 
Authorization  :   Bearer <Token>

```



# NOTE :-  Token will be use in :-
```
1) UserProfile Access
2)
```



#  PASSWORD_RESET_TIMEOUT  
```
PASSWORD_RESET_TIMEOUT = 900

```


# Email Send Process :-
```
// .env install for security  source :- https://github.com/jpadilla/django-doten
pip install django-dotenv
// put in manage.py
import dotenv
// write inside f() of manage.py
dotenv.read_dotenv()



// write code in .env file in chile project
EMAIL_USER = 'ankushgupta0510@gmail.com'
EMAIL_PASS = '123456'                          # write email password
EMAIL_FROM = 'ankushgupta0510@gmail.com'



// emai configuration put in seeting.py
import os
EMAIL_BACKEND = "django.core.mail.backends.mail.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')  # access value of EMAIL_USER From .env file 
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
EMAIL_USE_TLS = True



// make  other file utils.py in project app  and write your code.



// then in gmail account 'ankushgupta0510@gmail.com' enable like this  :-

Enhanced Safe Browsing for your account 
Less secure app access




```



#  Django email configuration
```
// source :-  https://docs.djangoproject.com/en/5.1/topics/email/
```



# Chatgpt Integrate
```
https://platform.openai.com/settings/profile?tab=api-keys


// fire this coomand 
pip install openai==0.28



//  write in setting.py
import os
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')



// write in a views.py

import openai
from django.shortcuts import render
from django.http import JsonResponse

# Function to call OpenAI's API
def chat_with_gpt(request):
    if request.method == "POST":
        user_input = request.POST.get('user_input')  # Get input from the user

        # Call OpenAI API
        openai.api_key = 'your-openai-api-key'
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input},
                ]
            )

            # Extract the model's response
            gpt_response = response['choices'][0]['message']['content']
            
            return JsonResponse({'response': gpt_response})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    
    return render(request, 'chat.html')

```




# download for imageField uploading
```
python -m pip install Pillow
```







### Media file importants for images
```

// import bellow all code in settings.py of djangoauthapi apps
import os
STATIC_URL = '/static/'      // ye JavaScript CSS HTML ke liye hota hai 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')     // ye django ki admin wali file hai

STATICFILES_DIR ={
    os.path.join(BASE_DIR, 'public/static')   //  if we upload photo then photo will be uploaded in 'public/static' directory
}

// below both line for media files example PDF, JPG etc.
MEDIA_ROOT = os.path.join(BASE_DIR, "public/static")    
MEDIA_URL = '/media/'



// import bellow all code in urls.py of djangoauthapi apps
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  // import in header


// import in footer
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

```



#  import it in form tag bcz it help to upload the image
```
enctype="multipart/form-data"
```




# install cv2 for image convert into array 
```
pip install opencv-python

```



# import model DL of EyeDisease Predictions
```
from tensorflow.keras.models import load_model
model = load_model('/content/drive/MyDrive/Eye Disease Prediction Dataset/Eye_Disease_DL_Model.h5')

import cv2
import matplotlib.pyplot as plt
test_img = cv2.imread('/content/drive/MyDrive/Eye Disease Prediction Dataset/SplitDataset/testdataset/cataract/0_left.jpg')
plt.imshow(test_img)


test_img = cv2.resize(test_img,(256,256))
test_input = test_img.reshape((1,256,256,3))
model.predict(test_input)
```


# install tensorflow
```
pip install tensorflow
pip show tensorflow
```


