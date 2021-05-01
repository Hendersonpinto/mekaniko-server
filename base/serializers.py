from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Brand, CarModel, Category, Service


# The name is setup by convention to <Model>Serializer
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    # We have 3 ways of defining nested relationships here:

    # FIRST WAY: Passing the serializer (defined before) as our field
    # categories = CategorySerializer(many=True)

    # SECOND WAY: Using Hyperlinked field to return the endpoint for the field. In this case, we need to also specify the context in our views!!
    categories = serializers.HyperlinkedRelatedField(many=True,
                                                     read_only=True,
                                                     view_name="category-detail")

    class Meta:
        model = Service
        fields = '__all__'

        # THIRD WAY: We can use depth, so we get full objects at the depth-level specified here.
        # This value specify how many levels we want our nested relationship to be explicit
        # In this case instead of showing the pk for the foreignKey fields, we show the entire object in the first depth-level
        # depth = 1
