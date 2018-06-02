from django.contrib import admin

from books.models import Book, BookNote
from django.db.models import Count


class BookNoteInline(admin.TabularInline):
    model = BookNote


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'percentage', 'number_of_pages', 'number_of_notes')
    inlines = [
        BookNoteInline,
    ]

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


admin.site.register(Book, BookAdmin)
admin.site.register(BookNote, BookNoteAdmin)
