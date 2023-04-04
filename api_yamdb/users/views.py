from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from api_yamdb.settings import CONTACT_EMAIL
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist

from api.v1.permissions import IsAdminOrSuperUser
from api.v1.serializers import (SignUpSerializer, UserSignUpSerializer, UserSignUpValidationSerializer,
                                TokenSerializer, UserSerializer,
                                UserEditSerializer)

from .utils import generate_confirmation_code, send_confirmation_code

User = get_user_model()


class RegisterView(APIView):
    """Регистирирует пользователя и отправляет ему код подтверждения."""
    permission_classes = (AllowAny,)

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get(
                username__iexact=username, email__iexact=email)
        except ObjectDoesNotExist:
            user_serializer = UserSignUpValidationSerializer(data=request.data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        mail_subject = 'Ваш код подтверждения для получения API токена'
        message = f'Код подтверждения - {confirmation_code}'
        send_mail(mail_subject, message, CONTACT_EMAIL, (email, ))
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    @action(
        methods=['patch', 'get'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserEditSerializer(user)
        if request.method == 'PATCH':
            serializer = UserEditSerializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
