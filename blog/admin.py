from django.contrib import admin

from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish', 'status', 'author')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    show_facets = admin.ShowFacets.ALWAYS
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'email', 'active', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('name', 'email', 'body')
    raw_id_fields = ('post',)
    date_hierarchy = 'created'
    ordering = ('created',)