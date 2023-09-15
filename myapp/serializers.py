from rest_framework import serializers
from django.db import IntegrityError
from rest_framework import serializers
from .models import *
from .api_exceptions import *

# I wrote this code -------------------------- Start
class UserGallerySerializer(serializers.ModelSerializer):
    '''UserGallerySerializer
    A serializer. UserGalleries serializer  

    Fields:
    - id : PK
    - gallery_image : File / Path

    Amendments:
    - user : user sessions id (This gets added when creating the serializer)
    '''
    class Meta:
        model = UserGalleries
        fields = ['id','gallery_image']

    def create(self, validated_data):
        validated_data['user'] = User.objects.get(id=self.context['request'].user.id)
        try:
            return UserGalleries.objects.create(**validated_data)
        except IntegrityError:
            raise BadRequestException("Integrity error")

class UserGalleriesSerializer(serializers.ModelSerializer):
    '''UserGalleriesSerializer
    A serializer. UserGalleries serializer

    Fields:
    - id : PK
    - gallery_image : File / Path
    - gallery_image_thumb : File / Path
    '''
    class Meta:
        model = UserGalleries
        fields = ['id','gallery_image', 'gallery_image_thumb']

class UserDetailsSerializer(serializers.ModelSerializer):
    '''UserDetailsSerializer
    A serializer. UserDetails serializer

    Fields:
    - profile_image : PK
    - about_me : String
    '''
    class Meta:
        model = UserDetails
        fields = ['profile_image', 'about_me']

class UserSerializer(serializers.ModelSerializer):
    '''UserSerializer
    A serializer. User serializer

    Fields:
    - id : PK
    - username : String
    - email : String
    - first_name : String
    - last_name : String
    - UserDetails : UserDetailsSerializer
    - UserGalleries : UserGalleriesSerializer
    - UserStatuses : UserStatusesSerializer
    '''
    UserDetails = UserDetailsSerializer()
    UserGalleries = serializers.SerializerMethodField()
    UserStatuses = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'UserDetails', 'UserGalleries', 'UserStatuses']

    def get_UserGalleries(self, obj):
        try:
            user_galleries = obj.UserGalleries.filter(user=obj)
            return UserGalleriesSerializer(user_galleries, many=True).data
        except UserGalleries.DoesNotExist:
            return None
        
    def get_UserStatuses(self, obj):
        try:
            user_statuses = obj.UserStatuses.filter(user=obj)
            return UserStatusesSerializer(user_statuses, many=True).data
        except UserStatuses.DoesNotExist:
            return None

class UserConnectionJunctionSerializer(serializers.ModelSerializer):
    '''UserConnectionJunctionSerializer
    A serializer. UserConnectionJunction serializer

    Fields:
    - id : PK
    - user_connection : PK

    Amendments:
    - user : user sessions id (This gets added when creating the serializer)
    '''
    class Meta:
        model = UserConnectionJunctions
        fields = ['id', 'user_connection']

    def create(self, validated_data):
        validated_data['user'] = User.objects.get(id=self.context['request'].user.id)
        try:
            return UserConnectionJunctions.objects.create(**validated_data)
        except IntegrityError:
            raise BadRequestException("Integrity error")

class UserStatusesSerializer(serializers.ModelSerializer):
    '''UserStatusesSerializer
    A serializer. UserStatuses serializer

    Fields:
    - id : PK
    - status : String

    Amendments:
    - user : user sessions id (This gets added when creating the serializer)
    '''
    class Meta:
        model = UserStatuses
        fields = ['id', 'status']

    def create(self, validated_data):
        validated_data['user'] = User.objects.get(id=self.context['request'].user.id)
        try:
            return UserStatuses.objects.create(**validated_data)
        except IntegrityError:
            raise BadRequestException("Integrity error")

class UserConnectionJunctionsSerializer(serializers.ModelSerializer):
    '''UserConnectionJunctionsSerializer
    A serializer. UserConnectionJunctions serializer

    Fields:
    - id : PK
    - user : UserSerializer
    - user_connection : UserSerializer
    '''
    user = UserSerializer()
    user_connection = UserSerializer()

    class Meta:
        model = UserConnectionJunctions
        fields = ['id', 'user', 'user_connection']

class ThreadSerializer(serializers.ModelSerializer):
    '''ThreadSerializer
    A serializer. Thread serializer

    Fields:
    - id : PK
    - title : String

    Amendments:
    - creating_user : user sessions id (This gets added when creating the serializer)
    '''
    class Meta:
        model = Threads
        fields = ['id', 'title']

    def create(self, validated_data):
        validated_data['creating_user'] = User.objects.get(id=self.context['request'].user.id)
        try:
            thread = Threads.objects.create(**validated_data)
            UserThreadJunctions.objects.create(user=validated_data['creating_user'], thread= thread)
            return thread
        except IntegrityError:
            raise BadRequestException("Integrity error")
        
class ThreadsSerializer(serializers.ModelSerializer):
    '''ThreadsSerializer
    A serializer. Threads serializer

    Fields:
    - id : PK
    - title : String
    - creating_user : UserSerializer
    '''
    creating_user = UserSerializer()

    class Meta:
        model = Threads
        fields = ['id', 'title', 'creating_user']

class UserThreadJunctionSerializer(serializers.ModelSerializer):
    '''UserThreadJunctionSerializer
    A serializer. UserThreadJunction serializer

    Fields:
    - id : PK
    - user : PK
    - thread : PK
    '''
    class Meta:
        model = UserThreadJunctions
        fields = ['id', 'user', 'thread']

class UserThreadJunctionsSerializer(serializers.ModelSerializer):
    '''UserThreadJunctionsSerializer
    A serializer. UserThreadJunctions serializer

    Fields:
    - id : PK
    - user : UserSerializer
    - thread : ThreadSerializer
    '''
    user = UserSerializer()
    thread = ThreadSerializer()
    class Meta:
        model = UserThreadJunctions
        fields = ['id', 'user', 'thread']

class ThreadMessagesSerializer(serializers.ModelSerializer):
    '''ThreadMessagesSerializer
    A serializer. ThreadMessages serializer

    Fields:
    - id : PK
    - thread : ThreadSerializer
    - creating_user : UserSerializer
    - message : String 
    '''
    thread = ThreadSerializer()
    creating_user = UserSerializer()
    class Meta:
        model = ThreadMessages
        fields = ['id', 'thread', 'creating_user', 'message']
# I wrote this code -------------------------- End