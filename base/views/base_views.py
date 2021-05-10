from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.permissions import IsAdminUserOrReadOnly
from base.models import Brand, CarModel, Category, Service, Shop
from base.serializers import BrandSerializer, CarModelSerializer, CategorySerializer, ServiceSerializer, ShopSerializer

from rest_framework import status

# DRF provides two wrappers to write our API views: the @api_view decorator for function based views and APIView classes for class based views


@api_view(['GET'])
def brandList(request):
    # This will return an queryset, which it's not compatible with JSON so I need to serialize it
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    # The Response class is an HttpResponse that allows its data to be rendered into arbitrary media types. Choosing the right type based on the type of the incoming request, like JSON, XML, HTML
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


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUserOrReadOnly])
def shopListCreate(request):
    # If the user is admin get access to both methods, otherwise only to GET due to IsAdminUserOrReadOnly permission
    if request.method == "GET":
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        serializer = ShopSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def shopDetail(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    serializer = ShopSerializer(shop, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def shopCreate(request):
    data = request.data
    serializer = ShopSerializer(data=data, context={'request': request})

    # https://stackoverflow.com/questions/67452173/django-rest-framework-field-serializer-validation-is-not-being-called
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def brandCreate(request):
    data = request.data
    try:
        brand = Brand.objects.create(
            name=data['name'],
        )
        serializer = BrandSerializer(brand, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Brand is not created'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
