from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


from .models import Brand, CarModel, Category, Service
from .serializers import BrandSerializer, CarModelSerializer, CategorySerializer, ServiceSerializer, UserSerializer, UserSerializerWithToken

# This is used to customize our tokens
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# DRF provides two wrappers to write our API views: the @api_view decorator for function based views and APIView classes for class based views

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    # NOTE: This is pretty tricky. Since we have set the authentication system to be simplejwt and we are using our api decorator
    # The user stored in request.user does NOT have to be the same user we log in using Django's admin interface.
    # Therefore, we need to pass the access token in our authorization header in order to get a response with our user profile data (request.user). SO YOU COULD BE LOGGED IN WITH DJANGO'S DEFAULT AUTH SYSTEM BUT IT WON'T FIND REQUEST.USER IF YOU DONT PASS THE TOKEN IN YOUR HEADERS
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def userList(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def brandList(request):
    # This will return an queryset, which it's not compatible with JSON so I need to serialize it
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def brandDetail(request, pk):
    # By using this shortcut, I don't have to define the 404 handling if the record is not found.
    brand = get_object_or_404(Brand, pk=pk)
    serializer = BrandSerializer(brand, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def carModelList(request):
    car_models = CarModel.objects.all()
    serializer = CarModelSerializer(car_models, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def carModelDetail(request, pk):
    car_model = get_object_or_404(CarModel, pk=pk)
    serializer = CarModelSerializer(car_model, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def categoryList(request):
    service_categories = Category.objects.all()
    serializer = CategorySerializer(service_categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def categoryDetail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def serviceList(request):
    services = Service.objects.all()
    # I need to add context if the hyperlinkfield relation is used in the serializer
    serializer = ServiceSerializer(
        services, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def serviceDetail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    serializer = ServiceSerializer(
        service, many=False, context={'request': request})
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
