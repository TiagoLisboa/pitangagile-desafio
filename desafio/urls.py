from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
from desafio.core import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('me/', views.UserView.as_view(), name='me')
]
