from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.v1.users.views import RegisterView, TokenView, UserViewSet

from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet,
)


app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')


urlpatterns_auth = [
    path('signup/', RegisterView.as_view()),
    path('token/', TokenView.as_view())
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(urlpatterns_auth)),
]
