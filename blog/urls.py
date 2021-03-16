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

from blog.views.AccountView import LoginView, LogoutView, SignupView
from blog.views.CommunityView import CommunityCreateView, CommunityDeleteView, CommunityListView, CommunityUpdateView
from blog.views.LanguageView import LanguageListView
from blog.views.PostView import PostListView, PostListByLanguageView, PostListByTagView
from blog.views.TagView import TagListView
from blog.views.UserView import UserDetailView, UserUpdateView

urlpatterns = [

    path('api/', include([

        path('account/', include([
            path('signup/', SignupView.as_view(), name='api.account.signup'),
            path('login/', LoginView.as_view(), name='api.account.login'),
            path('logout/', LogoutView.as_view(), name='api.account.logout'),
        ])),

        path('community/', include([
            path('create/', CommunityCreateView.as_view(), name='api.community.create'),
            path('list/', CommunityListView.as_view(), name='api.community.list'),
            path('<str:uuid>/update/', CommunityUpdateView.as_view(), name='api.community.update'),
            path('<str:uuid>/delete/', CommunityDeleteView.as_view(), name='api.community.delete'),
        ])),

        path('language/', include([
            path('list/', LanguageListView.as_view(), name='api.language.list'),
        ])),

        path('post/', include([
            path('list/', include([
                path('', PostListView.as_view(), name='api.post.list'),
                path('by_tag/<slug:slug>', PostListByTagView.as_view(), name='api.post.list.by_tag'),
                path('by_language/<slug:slug>', PostListByLanguageView.as_view(), name='api.post.list.by_language'),
            ])),
        ])),

        path('tag/', include([
            path('list/', TagListView.as_view(), name='api.tag.list'),
        ])),

        path('user/', include([
            path('<str:uuid>/', UserDetailView.as_view(), name='api.user.detail'),
            path('<str:uuid>/update/', UserUpdateView.as_view(), name='api.user.update'),
        ])),
    ])),

]
