from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView as TOP
from rest_framework.pagination import LimitOffsetPagination



from .views import (CategoryViewSet, ReviewViewSet, CommentViewSet)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
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
    path('v1/auth/token/', TOP.as_view(), name='token_obtain_pair'),
    path('v1/auth/signup/', )
]
