from django.contrib import admin
from .models import Shelf, Book


class BookInline(admin.TabularInline):
    model = Book
    extra = 0

class ShelfAdmin(admin.ModelAdmin):
    list_display = ('title','created','description')
    # filter_horizontal = ('customers',)
    list_filter = ('hidden',)
    fieldsets = [
        (None,               {'fields': ['title','description','created',]}),
        # ('Choices',       {'fields': ['typeof',]}),
        ('Access',       {'fields': ['hidden',]}),
    ]
    inlines = [BookInline]
    search_fields=['title','description']

class BookAdmin(admin.ModelAdmin):
	list_filter = ('typeof','hidden',)
	list_display = ('name', 'typeof','created','hidden',)


admin.site.register(Book,BookAdmin)
admin.site.register(Shelf,ShelfAdmin)