from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (UserInfoView, LoginView, RegisterView, 
                        VisitorViewSet, EmployeeViewSet, AccessRegisterViewSet)

router = DefaultRouter()
# Register your API endpoints here.
router.register('visitors', VisitorViewSet, basename='visitors'),
router.register('employees', EmployeeViewSet, basename='employees'),
router.register('access-registers', AccessRegisterViewSet, basename='access-registers'),


# Define the URL patterns for your API
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/user/', UserInfoView.as_view(), name='user_info'),
]