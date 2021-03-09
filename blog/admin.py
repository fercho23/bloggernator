from django.contrib import admin

from blog.models.User import User
from blog.models.Language import Language
from blog.models.Category import Category
from blog.models.Tag import Tag
from blog.models.Post import Post


admin.site.register(User)
admin.site.register(Language)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
