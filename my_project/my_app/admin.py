from django.contrib import admin
from .models import Post, Comment

@admin.action(description='Удалить контент')
def del_content(modeladmin, request, queryset):
    queryset.update(content = '') 

@admin.action(description=' Сделать заголовки апепркейсом')
def upper_titles(modeladmin, request, queryset):
    for post in queryset:
        post.title = post.title.upper()
        post.save()

@admin.action(description='Сделать заголовки ловеркейсом')
def lower_title(modeladmin, request, queryset):
    for post in queryset:
        post.title = post.title.lower()
        post.save()

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1





class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',    
        'author',
        'short_content',
        'len_content',
        'created_at',
    )

    list_filter = (
        'author',
        'created_at'
    )
    
    search_fields = (
        'content',
        'title',
    )

    def len_content(self, obj):

        return len(obj.content.count)
    
    len_content.short_description = 'Длина контента'

    def short_content(self, obj):
        if obj.content.__len__() > 50:
            return obj.content[:50] + '...'
        return obj.content
    short_content.short_description = 'Контент'



    ordering = ('-created_at',)

    inlines = [CommentInline]
    actions = [del_content, upper_titles, lower_title]


admin.site.register(Post, PostAdmin)

# Register your models here.
