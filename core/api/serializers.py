from rest_framework import serializers
from app.models import Posts
from account.models import CustomUser
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token

class PostSerilizers(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id','author','content','screenshot']


class AccountSerializer(serializers.ModelSerializer):
    email =serializers.CharField(max_length=50)
    first_name= serializers.CharField(max_length=30)
    last_name= serializers.CharField(max_length=30)
    password =serializers.CharField(min_length=8,write_only=True)
    class Meta:
        model =CustomUser
        fields =['email','first_name','last_name','password']

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
