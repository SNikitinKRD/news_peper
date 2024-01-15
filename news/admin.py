from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'type_post', 'title', 'date_create')
    list_filter = ('author', 'type_post', 'category')
    search_fields = ('author__user__username', 'category__name')
    #actions = [nullfy_quantity] # добавляем действия в список

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(CategorySubscribers)

# Register your models here.
