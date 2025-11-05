from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from rest_framework.authtoken import views as token_views



router = DefaultRouter()
router.register(r'users', UserViewSet,basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
     path('login/', token_views.obtain_auth_token, name='login'),  # 登录获取token的路径

]