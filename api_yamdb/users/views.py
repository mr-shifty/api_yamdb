from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.permissions import IsAdminOrSuperUser
from api.v1.serializers import (AuthorSerializer, SignUpSerializer,
                                TokenSerializer, UserSerializer)

from .utils import generate_confirmation_code, send_confirmation_code

User = get_user_model()


class RegisterView(APIView):
    """Регистирирует пользователя и отправляет ему код подтверждения."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid()
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        if serializer.is_valid():
            confirmation_code = generate_confirmation_code()
            user = User.objects.filter(email=email).exists()
            if not user:
                User.objects.create_user(email=email, username=username)
                User.objects.filter(email=email).update(
                    confirmation_code=generate_confirmation_code())
                send_confirmation_code(email, confirmation_code)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                'Такой пользователь уже зарегистирован',
                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    """Проверяет код подтверждения и отправляет токен."""
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(
            User,
            username=username,
        )
        if user.confirmation_code != confirmation_code:
            return Response(
                'Confirmation code is invalid',
                status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response(
            {'access_token': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """Админ получает список пользователей или создает нового"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperUser, ]
    lookup_field = 'username'
    search_fields = ('username', )


class MeView(APIView):
    """Пользователь может посмотреть свой профиль и изменить его"""

    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(
            'Вы не авторизованы',
            status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            if request.user.role == 'admin':
                serializer = UserSerializer(
                    user,
                    data=request.data,
                    partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = AuthorSerializer(
                    user,
                    data=request.data,
                    partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return Response(
            'Вы не авторизованы',
            status=status.HTTP_401_UNAUTHORIZED)
