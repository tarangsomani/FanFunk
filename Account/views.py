from django.shortcuts import render
from Account.models import Users,ApiToken
from Account.serializers import UserSerializer,UserLoginSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView


class RegisterAPIView(APIView):

    def post(self,request):

        info=request.data
        create = UserSerializer(data=info)

        if create.is_valid():
            create.save()
            user=Users.objects.filter(email=info['email']).first()
            ApiToken.objects.create(user=user)
            token = ApiToken.objects.filter(user=user).first()
            token.create_token()
            token.save()
            dic={'user data':create.data,'token':token.api_token}
            return Response(dic,status=200)

        else:
            return Response({"error message":"signup failed"})


class LoginAPIView(APIView):

    def post(self,request):

        info = request.data
        valid_user = Users.objects.filter(email=info['email'],password=info['password']).first()
        #print(valid_user.name)
        if valid_user is not None:
            #object = Users.objects.filter(email=info['email'],password=info["password"]).first()
            token = ApiToken.objects.filter(user=valid_user).first()
            print(valid_user.id)

            if token is None:
                ApiToken.objects.create(user=valid_user)
                token = ApiToken.objects.filter(user=valid_user).first()
                token.create_token()

                token.is_valid = True
                token.save()
                dic = {'user data': UserSerializer(instance=valid_user).data, 'token': token.api_token}
                return Response(dic,status=200)

            elif token.is_valid is True:
                dic = {'user data': UserSerializer(instance=valid_user).data, 'token': token.api_token,"message":"already logged in"}
                return Response(dic,status=200)
            elif token.is_valid is False:
                #token.api_token = None
                #token.create_token()
                token.is_valid=True
                token.save()
                print("token activated")
                dic = {'user data': UserSerializer(instance=valid_user).data, 'token': token.api_token}
                return Response(dic,status=200)

            #print(token.is_valid)

        else:
            return Response({"error message":"Login Failed. Incorrect email or password"},status=400)


class LogOutAPIView(APIView):

    def get(self,request):

        token = request.query_params["TOKEN"]
        object = ApiToken.objects.filter(api_token=token).first()
        #print(object.api_token)
        if object is None:
            return Response({"message":"Invalid Token"},status=400)

        else:
            #object.user.push_notification_id = Null
            object.delete()
            return Response({"message":"successfully logged out"},status=200)





