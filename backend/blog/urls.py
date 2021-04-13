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

from rest_framework.authtoken import views
from rest_framework.authtoken.views import obtain_auth_token

from blog.views.AccountView import LoginView, LogoutView, SignupView
from blog.views.CommunityView import CommunityCreateView, CommunityDeleteView, CommunityCurrentUserListView, CommunityListView, CommunityReadView, CommunityUpdateView
from blog.views.LanguageView import LanguageListView
from blog.views.PostView import PostCreateView, PostDeleteView, PostListView, PostReadView, PostUpdateView
from blog.views.TagView import TagListView
from blog.views.UserView import UserDeleteView, UserReadView, UserUpdateView

urlpatterns = [

    path('account/', include([
        path('signup/', SignupView.as_view(), name='api.account.signup'),
        path('login/', LoginView.as_view(), name='api.account.login'),
        path('logout/', LogoutView.as_view(), name='api.account.logout'),

        path('token-auth/', obtain_auth_token, name='api_token_auth'),
    ])),

    path('community/', include([
        path('create/', CommunityCreateView.as_view(), name='api.community.create'),
        path('current_user/list/', CommunityCurrentUserListView.as_view(), name='api.community_current_user.list'),
        path('list/', CommunityListView.as_view(), name='api.community.list'),
        path('<str:slug>/', CommunityReadView.as_view(), name='api.community.read'),
        path('<str:slug>/delete/', CommunityDeleteView.as_view(), name='api.community.delete'),
        path('<str:slug>/update/', CommunityUpdateView.as_view(), name='api.community.update'),
    ])),

    path('language/', include([
        path('list/', LanguageListView.as_view(), name='api.language.list'),
    ])),

    path('post/', include([
        path('create/', PostCreateView.as_view(), name='api.post.create'),
        path('list/', PostListView.as_view(), name='api.post.list'),
        path('<str:slug>/', PostReadView.as_view(), name='api.post.read'),
        path('<str:slug>/delete/', PostDeleteView.as_view(), name='api.post.delete'),
        path('<str:slug>/update/', PostUpdateView.as_view(), name='api.post.update'),
    ])),

    path('tag/', include([
        path('list/', TagListView.as_view(), name='api.tag.list'),
    ])),

    path('user/', include([
        path('<str:username>/', UserReadView.as_view(), name='api.user.read'),
        path('<str:username>/update/', UserUpdateView.as_view(), name='api.user.update'),
        path('<str:username>/delete/', UserDeleteView.as_view(), name='api.user.delete'),
    ])),

]
