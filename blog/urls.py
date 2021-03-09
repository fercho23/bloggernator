"""bloggernator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path

from blog.views.AccountView import LoginView, SignupView
from blog.views.UserView import UserDetailView, UserUpdateView

urlpatterns = [


    path('api/', include([

        path('account/', include([
            path('signup/', SignupView.as_view(), name='api.account.signup'),
            path('login/', LoginView.as_view(), name='api.account.login'),
            # path('logout/', LogoutView.as_view(), name='api.account.logout'),
        ])),

        path('user/', include([
            path('<str:pk>/', UserDetailView.as_view(), name='api.user.detail'),
            path('<str:pk>/update/', UserUpdateView.as_view(), name='api.user.update'),
        ])),

        path('post/', include([
        ])),

        path('tag/', include([
        ])),

        path('category/', include([
        ])),

        path('language/', include([
        ])),
    ])),

]
