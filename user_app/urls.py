from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenBlacklistView
from .views import DashboardView
from user_app.views import logout_view
from django.urls import path

urlpatterns = [


    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('logout/', logout_view.as_view(), name='logout'),
]