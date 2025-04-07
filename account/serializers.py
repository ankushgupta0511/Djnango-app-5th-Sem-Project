from rest_framework import serializers
from account.models import User

# import util file 
from account.utils import Util


# import for email changing liberary
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator



class UserRegistrationSerializer(serializers.ModelSerializer):

    # We are writing this bcz we need confirm password field in our Registration Request
    # ye likhne se password dot dot ke form mai dikhega
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)   # 'write_only=True' means we add in a model
    # print('\n\n\nankush serializers\n\n\n')

    class Meta:
        model = User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }
        
        
    # Validating Password and Confirm Password while Registration
    # attrs is also called data
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        # print(password,password2)
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't Match!!" )

        return attrs
    
    
    
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
        
        

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']
     
     
     
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']
        
        

class UserChangePasswordViewSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)  # 'write_only=True' means we add in a model 
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True) # 'write_only=True' means we add in a model
    class Meta:
        fields = ['password','password2']

    
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')  # here we write  context bcz 'user' come in a context 
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't Match!!" )
        
        user.set_password(password)   
        user.save()
        return attrs



class SendPasswordResetEmailViewSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email']
        
    
    def validate(self,attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print('original id : ',user.id)
            uid = urlsafe_base64_encode(force_bytes(user.id))    # genrate uid based on user ID
            # 'urlsafe_base64_decode' not take integer value thus we use 'force_bytes'
            # 'force_bytes' convert into interger num. to bytes then bytes convert into encode.

            print('Encoded uid id : ',uid)
            token = PasswordResetTokenGenerator().make_token(user)   # genrate token base on user
            print(token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link :-  ',link)

            # Send Email
            body = 'Click Following Link to Reset Your Password :- '+ link
            data = {
                'subject' : "Reset You Password!",
                'body':body,
                'to_email':user.email
            }
            
            Util.send_email(data)
            print('\n UtilDone \n')
            return attrs
        else:
            raise serializers.ValidationError("User Not Ragistered!!" )
        
        
        
        
        
        
class UserPasswordResetViewSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)  # 'write_only=True' means we add in a model 
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True) # 'write_only=True' means we add in a model
    class Meta:
        model = User
        fields = ['password','password2']

    
    def validate(self,attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')  # here we write  context bcz 'uid' come in a context 
            token = self.context.get('token')  # here we write  context bcz 'token' come in a context 
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't Match!!" )
            
            # decode 'uid'
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            
            # check token base on user and this token genrated code written in above class f()  'SendPasswordResetEmailViewSerializer'
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValueError('Token is not Valid or Expired11!!')
                
            user.set_password(password)   
            user.save()
            return attrs
        
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValueError('Token is not Valid or Expired22!!')
            
            
            
    
