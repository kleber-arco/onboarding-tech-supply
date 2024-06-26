"""
URL configuration for onboarding_tech_supply project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog.views import PostList, UpdateAutor, SpecificPost, KeycloakGenerateToken, KeycloakValidateToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/posts/', PostList.as_view(), name='post-list'),
    path('api/v1/posts/update-autor/<int:post_id>/', UpdateAutor.as_view(), name='update-autor'),
    path('api/v1/posts/<int:post_id>/', SpecificPost.as_view(), name='specific-post'),
    path('api/v1/token/generate/', KeycloakGenerateToken.as_view(), name='keycloak-generate-token'),
    path('api/v1/token/validate/', KeycloakValidateToken.as_view(), name='keycloak-validate-token')
]
