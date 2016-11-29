from django.contrib import admin

from books.models import Book, BookNote


class BookAdmin(admin.ModelAdmin):
    pass


class BookNoteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(BookNote, BookNoteAdmin)
