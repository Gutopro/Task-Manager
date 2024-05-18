from rest_framework import serializers
from .models import UserModel
from django.contrib.auth.hashers import make_password

class UserModelSerializer(serializers.ModelSerializer):
    """ Serializer for user model """
    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, validated_data):
        """ hashes a password before saving in the database """
        password = make_password(validated_data['password'])
        validated_data['password'] = password
        return UserModel.objects.create(**validated_data)

class UserModelUpdateSerializer(UserModelSerializer):
    """ Serializer for updating an existing user """
    class Meta:
        model = UserModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserModelUpdateSerializer, self).__init__(*args, **kwargs)
        # Make field optional when updating
        for field_name, field in self.fields.items():
            field.required = False
