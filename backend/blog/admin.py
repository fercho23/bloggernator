from django.contrib import admin

from blog.models.User import User
from blog.models.Community import Community
from blog.models.Language import Language
from blog.models.Tag import Tag
from blog.models.Post import Post


admin.site.register(User)
admin.site.register(Community)
admin.site.register(Language)
admin.site.register(Tag)
admin.site.register(Post)
