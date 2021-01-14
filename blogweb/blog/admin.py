from django.contrib import admin
from blog.models import Post ,Comment 
from blog.models import Category

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)