from django.urls import include, path
from rest_framework import routers
from desafio.core import views

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('me/', views.UserView.as_view(), name='me')
]
