from rest_framework import serializers
from .models import User

class CreateUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(required= True, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ( 'username',  'email',  'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class CheckUserSerializer(serializers.Serializer):

    email  = serializers.EmailField(required = True, write_only=True, label ='Email address')
    password = serializers.CharField(required= True, write_only=True, style={'input_type': 'password'})
    class Meta:
        fields = ('username', 'email',  'password')
