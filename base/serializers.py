from rest_framework import serializers
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Brand, CarModel, Category, Service, Shop
from rest_framework.fields import CurrentUserDefault


# The name is by convention: <Model>Serializer
class UserSerializer(serializers.ModelSerializer):
    # Instead of modifying the User model we add a new field to our serializer using a method field.
    name = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin']

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name

    def get_isAdmin(self, obj):
        return obj.is_staff


class UserSerializerWithToken(UserSerializer):
    # We are creating a user serializer with a token included, we will use this serializer when new users register in our app so the token is returned in the response so we can log them at once.
    # Otherwise, users would need to register and then log in (obtain the token) for future actions
    # SerializerMethodField are used to add fields that are usually not declared in our models
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

    def validate_name(self, value):
        print(value)
        """
        Check that the brand name has at least 20 characters
        """
        if len(value) < 20:
            raise serializers.ValidationError(
                "The name of the brand should be longer than 20 characters")
        return value


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


class ShopSerializer(serializers.ModelSerializer):
    # This will hide the owner field from the response and take the current logged user as default value
    # owner = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )

    # This will use our UserSerializer to serialize our response back and in case there is no "owner" key in the request body, we will use the currentUserDefault(). If we want to use another user but the information is not included in the request.body we need to override the create method inside of the UserSerializer
    owner = UserSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = Shop
        fields = '__all__'
        # depth = 1

# https://stackoverflow.com/questions/41894346/how-to-send-post-data-to-nested-serializer-django-rest-framework
# https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations

    def create(self, validated_data):
        # Since lat and lon are not defined in our model, they won't be included in our "validated_data". Therefore I need to pass them in the context!
        # dict.get() If given key exists in the dictionary, then it returns the value associated with this key, If given key does not exists in dictionary, then it returns the passed default value argument. If given key does not exists in dictionary and Default value is also not provided, then it returns None.

        lat = self.context['request'].data.get('lat')
        lon = self.context['request'].data.get('lon')

        if lon and lat:
            validated_data['location'] = Point(
                int(lon), int(lat))
        else:
            validated_data['location'] = Point(0, 0)

        # if 'owner' not in validated_data:
        #     # https://stackoverflow.com/questions/30203652/how-to-get-request-user-in-django-rest-framework-serializer
        #     validated_data['owner'] = self.context['request'].user

        # Or: owner = self.context['request'].user
        # instance = Shop.objects.create(owner=owner, **validated_data)

        instance = Shop.objects.create(**validated_data)

        return instance

    def validate_name(self, value):
        print(value)
        """
        Check that the shop name has at least 20 characters long
        """
        if len(value) < 20:
            print(value)
            raise serializers.ValidationError(
                "The name of the shop should be longer than 20 characters")
        return value

    def validate(self, data):
        print("whatever")
        if not data['city']:
            raise serializers.ValidationError(
                "The city should be defined")
        return data
