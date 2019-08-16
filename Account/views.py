from django.shortcuts import render
from Account.models import Users, ApiToken, UserDevice,PushNotification
from Account.serializers import UserSerializer,UserLoginSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class RegisterAPIView(APIView):

    def post(self, request):
        info = request.data['info']
        create = UserSerializer(data=info)
        user_exists = Users.objects.filter(email=info['email']).first()

        if user_exists:
            return Response({"Message": "User already exists"})

        if create.is_valid():
            create.save()
            user = Users.objects.filter(email=info['email']).first()
            ApiToken.objects.create(user=user)
            token = ApiToken.objects.filter(user=user).first()
            token.create_token()
            token.save()
            UserDevice.objects.create(user=user,device_id=request.data['device_id'])
            PushNotification.objects.create(user=user,push_notification_id=request.data['push_notification_id'])
            dic = {'user data': create.data,'token': token.api_token}
            return Response(dic, status=200)

        elif create.is_valid is False:
            return Response({"error message": "Data not in required format"})

        else:
            return Response({"error message": "signup failed"})


class LoginAPIView(APIView):

    def post(self, request):
        info = request.data
        valid_user = Users.objects.filter(email=info['email'], password=info['password']).first()

        if valid_user is not None:
            token = ApiToken.objects.filter(user=valid_user).first()

            if token is None:
                ApiToken.objects.create(user=valid_user)
                token = ApiToken.objects.filter(user=valid_user).first()
                token.create_token()
                token.is_valid = True
                token.save()
                push_notification = PushNotification.objects.filter(user=valid_user).first()
                push_notification.create_notification_token()
                push_notification.save()
                dic = {'user data': UserSerializer(instance=valid_user).data, 'token': token.api_token}
                return Response(dic,status=200)

            elif token.is_valid is True:
                dic = {'user data': UserSerializer(instance=valid_user).data, 'token': token.api_token,"message": "already logged in"}
                return Response(dic, status=200)

            elif token.is_valid is False:
                token.is_valid = True
                token.save()
                dic = {'user data': UserSerializer(instance=valid_user).data, 'token': token.api_token}
                return Response(dic, status=200)

        else:
            return Response({"error message": "Login Failed. Incorrect email or password"}, status=400)


class LogOutAPIView(APIView):

    def get(self,request):
        token = request.query_params["TOKEN"]
        obj = ApiToken.objects.filter(api_token=token).first()

        if obj is None:
            return Response({"message": "Invalid Token"}, status=400)

        else:
            obj.delete()
            push_not = PushNotification.objects.filter(user=obj.user).first()
            push_not.push_notification_token = None
            return Response({"message": "successfully logged out"}, status=200)





