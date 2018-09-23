from django.contrib import admin
from django.db.models import Count

from .models import Book, BookNote, BookNameMapper, Favorite


class BookNoteInline(admin.TabularInline):
    model = BookNote


class BookAdmin(admin.ModelAdmin):
    fields = ('original_title', 'author', 'title', 'percentage', 'rating', 'number_of_pages',)
    list_display = ('proper_title', 'percentage', 'number_of_pages', 'number_of_notes', )
    inlines = [
        BookNoteInline,
    ]
    search_fields = (
        'title',
        'author',
        'original_title',
    )

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
                .prefetch_related('notes')
                .annotate(number_of_notes=Count('notes'))
        )

    def number_of_notes(self, obj):
        return obj.number_of_notes

    number_of_notes.admin_order_field = 'number_of_notes'


class BookNoteAdmin(admin.ModelAdmin):
    pass


class BookMapperAdmin(admin.ModelAdmin):
    pass


class FavoritesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(BookNote, BookNoteAdmin)
admin.site.register(BookNameMapper, BookMapperAdmin)
admin.site.register(Favorite, FavoritesAdmin)
