from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Brand, CarModel, Category, Service, Shop


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
    owner = UserSerializer(many=False)

    class Meta:
        model = Shop
        fields = '__all__'
