from django.shortcuts import render
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordViewSerializer,SendPasswordResetEmailViewSerializer,UserPasswordResetViewSerializer

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate # import here authenticate
from account.renderers import UserRenderer   # import custome errors

from rest_framework_simplejwt.tokens import RefreshToken  # import for authentication
from rest_framework.permissions import IsAuthenticated



# Genrating Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }




class UserRagistrationView(APIView):
    renderer_classes = [UserRenderer]   # ab all 'error' word show before error text
    def post(self, request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
        # if serializer.is_valid():
            user = serializer.save()
            
            token = get_tokens_for_user(user)   # calling to genrate tokens
            
            return Response({'token':token,'msg':'Registration Successfully!!'},status=status.HTTP_201_CREATED)
        
        #  'print(serializer.errors)' will be print errors in terminal if  'raise_exception=True' nahi  diya ho inside as a argument in a serializer.is_valid() and if argument diya ho to nahi prind honga error in terminal
        # print(serializer.errors) 
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]   # ab all 'error' word show before error text
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)   # auth will check user exist or not in DB. 
            if user is not None:
                token = get_tokens_for_user(user)   # calling to genrate tokens
                return Response({'token':token,'msg':'Login Success!!'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]   # ab all 'error' word show before error text

   # below line for genrating errors as a response if user not provide token or not provide needed credential during fetching data 
    permission_classes = [IsAuthenticated]     # this line means user shoud be login outherwise it show an error as a response
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)   # 'request.user' it give current user
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]   # ab all 'error' word show before error text

    # below line for genrating errors as a response if user not provide token or not provide needed credential during fetching data 
    permission_classes = [IsAuthenticated]   # this line means user shoud be login outherwise it show an error as a response 
    def post(self,request,format=None):
        serializer = UserChangePasswordViewSerializer(data = request.data,context = {'user':request.user})   # 'request.user' it give current user  with userprofile data which current have Login 
        
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Change Successfully!!'},status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    



class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]   # ab all 'error' word show before error text

    # below line for genrating errors as a response if user not provide token or not provide needed credential during fetching data 
    # permission_classes = [IsAuthenticated]   # this line means user shoud be login outherwise it show an error as a response 
    
    def post(self,request,format=None):
        print('\n SendPasswordResetEmailView1 \n')
        serializer = SendPasswordResetEmailViewSerializer(data = request.data)
        print(serializer)
        print('\n SendPasswordResetEmailView2 \n')
        if serializer.is_valid(raise_exception=True):
            print('\n SendPasswordResetEmailView3 \n')
            return Response({'msg':'Password Reset Link Send. Please Check Your Email!!'},status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        
        
        

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]   # ab all 'error' word show before error text

    # below F() take dynemic perameter like uid and token 
    def post(self,request,uid,token,format=None):
        print('\n UserPasswordResetView2221 \n')
        serializer = UserPasswordResetViewSerializer(data = request.data,context={'uid':uid,'token':token})
        print('\n  UserPasswordResetView2 \n')
        if serializer.is_valid(raise_exception=True):
            print('\n UserPasswordResetView3 \n')
            return Response({'msg':'Password Reset Successfully!!'},status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)