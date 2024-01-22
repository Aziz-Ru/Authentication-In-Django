from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .renderers import UserRenderers
from .serializers import *
from .models import User
from Account.utils import Utility


#Generate token manually

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegisterView(APIView):
    renderer_classes=[UserRenderers]
    def post(self,request):
        serializer=UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        username=serializer.data.get("username")
        email=serializer.data.get('email')
        Utility.send_otp_to_email(context={"username":username,"email":email})
        token=get_tokens_for_user(user)
        return Response({'msg':'Please Verify Your Account','token':token, 'status':status.HTTP_201_CREATED},status=status.HTTP_201_CREATED)
    

class UserAccountVerifyEmailView(APIView):
    renderer_classes=[UserRenderers]
    def post(self,request):
        serializer=VerifyUserAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
                'status':status.HTTP_200_OK,
                'message':"Your Account is Verified Now"
                },status=status.HTTP_200_OK)
        
             


class UserLoginView(APIView):
    renderer_classes=[UserRenderers]
    def post(self,request):
            serializer=UserLoginSerializer(data=request.data)
            # print(request.data.get('email'))
            serializer.is_valid(raise_exception=True)
            email=serializer.data.get('email')
            password=serializer.data.get('password')
                #  print(email+password)
            user=authenticate(email=email,password=password)
            if user is not None:
                verified_user=User.objects.get(email=email)
                if verified_user.is_verified==True:
                    token=get_tokens_for_user(user)
                    return Response({'token':token,'msg':'Login Successfully'},status=status.HTTP_200_OK)
                else:
                    return Response({'errors':{'non_fields_error':['Invalid User']}},status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'errors':{'non_fields_error':['Email or Password is not Valid']}},status=status.HTTP_400_BAD_REQUEST)
                      
                      
class UserProfileView(APIView):
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data ,status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated] 
    
    def post(self,request):
        serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Change Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SendPasswordChangeEmailView(APIView):
    renderer_classes=[UserRenderers]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message':'Password Reset Link Send . Please Check Your Email'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_200_OK)
        
class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderers]
    def post(self,request,uid,token):
        serializer=UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Change Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        


