from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from user.serializers import UserProfileSerializer, UserImageSerializer

User = get_user_model()


@api_view(["POST"])
def login(request):
    user = User.objects.filter(email=request.data.get("email"))
    if user:
        user = user[0]
        correct_pass = user.check_password(request.data.get("password"))
        if correct_pass:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': f"Token {token.key}", 'user_id': user.pk, 'email': user.email, "is_admin": user.is_superuser, "is_member": user.is_member}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "password didn't match"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "that email is not registered"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def signup(request):
    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def me(request):
    if type(request.user.id) == type(None):
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(UserProfileSerializer(get_user_model().objects.get(id=request.user.id)).data, status=status.HTTP_200_OK)


@api_view(["POST"])
def upload_profile_photo(request):
    if type(request.user.id) == type(None):
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        body = {
            "id": request.user.id,
            "profile_photo": request.data.get("profile_photo")
        }
        serializer = UserImageSerializer(
            get_user_model().objects.get(id=request.user.id), data=body)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
