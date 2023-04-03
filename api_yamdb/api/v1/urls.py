from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from users.views import MeView, RegisterView, TokenView, UserViewSet


app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')


urlpatterns_auth = [
    path('signup/', RegisterView.as_view()),
    path('token/', TokenView.as_view())
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(urlpatterns_auth)),
    path('v1/users/me/', MeView.as_view()),
]
