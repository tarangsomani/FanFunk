from Account.models import Users,ApiToken
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'


class UserLoginSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ['email','password']


class UserLogoutSerializer(ModelSerializer):

    class Meta:
        model = ApiToken
        fields = ['api_token']


class ApiTokenSerializer(ModelSerializer):

    class Meta:
        model = ApiToken
        fields = ['user']
