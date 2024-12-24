from django.contrib.staticfiles.views import serve
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Trang chủ
    path('login/', views.login_view, name='login'),  # Đăng nhập
    path('signup/', views.signup_view, name='signup'),  # Đăng ký
    path('logout/', views.logout_view, name='logout'),  # Đăng xuất
    path('account/', views.account_view, name='account'),  # Trang quản lý tài khoản
    path('favicon.ico', serve, {'path': 'favicon.ico'}),
]
