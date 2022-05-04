from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (
    ReviewViewSet,
    CommentViewSet,
    UserViewSet,
    UserRegistrationView as Registr,
    AuthTokenView as Auth
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='viewsets'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', Registr.as_view(), name='signup'),
    path('v1/auth/token/', Auth.as_view(), name='auth')
]
