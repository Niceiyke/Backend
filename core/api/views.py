from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import PostSerilizers,AccountSerializer,UpvoteSerializer
from app.models import Posts,Upvote

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(GenericAPIView):
    serializer_class=AccountSerializer

    def post(self,request:Request):
        data =request.data

        serializer =self.serializer_class(data=data)


        if serializer.is_valid():
            serializer.save()

            response={
                'message': 'User Created Successfully',
                'data':serializer.data
            }

            return Response(data=response,status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


class ListCreatePost(ListCreateAPIView):
    queryset =Posts.objects.all()
    serializer_class =PostSerilizers


class SinglePost(RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class =PostSerilizers
    lookup_fields = ['id']


class getPostUpvote(APIView):
    def get(self, request,pk, format=None):
        queryset = Upvote.objects.filter(post_id=pk)
        serializer=UpvoteSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request,pk, format=None):
            serializer = UpvoteSerializer(data=request.data)
            print ('data',serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

