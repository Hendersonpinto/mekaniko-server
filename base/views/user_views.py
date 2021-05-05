from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


from base.models import Brand, CarModel, Category, Service
from base.serializers import BrandSerializer, CarModelSerializer, CategorySerializer, ServiceSerializer, UserSerializer, UserSerializerWithToken

# This is used to customize our tokens
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status


@api_view(['POST'])
def registerUser(request):
    data = request.data

    # We need to handle the error, to give details to our users
    try:
        user = User.objects.create(
            # We will store both names in first name and use email as the username
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            # Passwords can't be sretored in the raw form. We need to hash it before add it to the DB
            password=make_password(data['password'])
        )
        # We use this serializer because we want to return the access token so we can log the user right after created
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    # NOTE: This is pretty tricky. Since we have set the authentication system to be simplejwt and we are using our api decorator
    # The user stored in request.user does NOT have to be the same user we log in using Django's admin interface.
    # Therefore, we need to pass the access token in our authorization header in order to get a response with our user profile data (request.user). SO YOU COULD BE LOGGED IN WITH DJANGO'S DEFAULT AUTH SYSTEM BUT IT WON'T FIND REQUEST.USER IF YOU DONT PASS THE TOKEN IN YOUR HEADERS
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    # We will use userSerializerWithToken because we will get a new access token when updating our profile
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    # We save outside of the if, because our users can edit their information without needing to send a new password
    user.save()

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def userList(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

    # ---------    Customization of our tokens and token response


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # We have two ways of customizing our tokens:
    # 1) Add the extra data to the response we get after login
    # 2) Add the extra data inside of the token itself (requires decoding the token in the client to consume this data)

    # This is the (1) way to add new extra fields (username, email) to the response we get after sending a POST request to our login endpoint.
    def validate(self, attrs):
        data = super().validate(attrs)

        # Instead of writing all the fields we need from the request.user, we can loop through the properties
        # data['username'] = self.user.username
        # data['email'] = self.user.username

        # Looping instead of writing all the data fields
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data

    # This is the (2) way to add new extra fields (username, email) to the encoded token itself (requires decoding the token).
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # This will add username and message fields to the encoded token
        token['username'] = user.username
        # token['message'] = 'Hello world'

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# ---------    Customization of our tokens and token response
