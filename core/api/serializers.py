from django.conf import settings
from rest_framework import serializers
from account.models import CustomUser
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from social.models import Post,UserProfile,Comment

class AccountSerializer(serializers.ModelSerializer):
    email =serializers.CharField(max_length=50)
    password =serializers.CharField(min_length=8,write_only=True)
    class Meta:
        model =CustomUser
        fields =['email','password']

    def validate(self,attrs):
        email_exist =CustomUser.objects.filter(email=attrs['email']).exists()

        if email_exist:
            raise ValidationError('Email has already been used')

        return super().validate(attrs)

    def create(self, validated_data):
        password=validated_data.pop('password')

        user=super().create(validated_data)

        user.set_password(password)
        user.save()

        Token.objects.create(user=user)

        return user

class PostSerializer(serializers.ModelSerializer):
    num_likes =serializers.SerializerMethodField(read_only=True)
    num_dislikes  =serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
        'post_id',
        'body','image',
        'expiration',
        'author',
        'likes',
        'num_likes',
        'num_dislikes',
        'dislikes',
        'created_on',
        'tags']

    def get_num_likes(self,obj):
     return obj.get_number_of_likes()
    def get_num_dislikes(self,obj):
     return obj.get_number_of_dislikes()

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model =UserProfile
        fields ='__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model =Comment
        fields ='__all__'

