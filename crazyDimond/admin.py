from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Article2tag)
admin.site.register(ArticleDetail)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(UporDown)
admin.site.register(Category)

