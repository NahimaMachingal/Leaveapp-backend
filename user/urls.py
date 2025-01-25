
from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('api/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('leave-requests/', LeaveRequestView.as_view(), name='leave-requests'),
    path('mleave-requests/', MleaveRequestView.as_view(), name='mleave-requests'),
    path('update-status/<int:leave_id>/', UpdateLeaveStatusView.as_view(), name='update-status'),

]
