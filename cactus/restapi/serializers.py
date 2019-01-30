from rest_framework import serializers
from usermodel.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation as validators
from django.core import exceptions
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar')
        read_only_fields = ('email', 'username', 'first_name', 'last_name', 'avatar')

class ModifySerializer(serializers.ModelSerializer):

    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required= False, max_length = 35, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'avatar', 'password' )

    def __init__(self, *args, **kwargs):
        super(ModifySerializer,self).__init__(*args, **kwargs)
        request = self.context['request']
        
        if request.method == 'POST':
            self.fields['password'].required = True
            self.fields['email'].required = True
            self.fields.pop('username')     # Lo toma del queryfield cuando es un post

        if request.method == 'PUT':
            self.fields.pop('email')    # Para cambiar el email hay que eliminar al usuario
            self.fields['password'].required = False    # No es necesario pero es por claridad
    # Utiliza las validaciones que hay en settings
    def validate_password(self, data):
            if data=='' : return super(ModifySerializer, self).validate(data)
            errors = dict() 
            try:
                validators.validate_password(password=data)
            except exceptions.ValidationError as e:
                errors['password'] = list(e.messages)
            if errors:
                raise serializers.ValidationError(errors)
            return super(ModifySerializer, self).validate(data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        if 'avatar' in validated_data:
            if validated_data['avatar'] != None:
                instance.avatar = validated_data.get('avatar', instance.avatar)
        
        instance.save()
        return instance

    def create(self, validated_data):
        user = User(email=validated_data['email'])
        validated_data['username']= self.context['user']
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)
